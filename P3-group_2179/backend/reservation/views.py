from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import ReservationSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Reservation
from django.views.decorators.csrf import csrf_exempt # Need to remove this line when validation is proper
from django.http import HttpResponse, JsonResponse
from property.models import Property
from datetime import date,timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from notification.models import Notification




def update_status(reservation):
    if reservation.status == 'A':
        if reservation.end<date.today():
            reservation.status='F'
            reservation.save()
    elif reservation.status == 'P':
        if ((reservation.start<date.today()) or reservation.created<date.today()-timedelta(days=3)):
            reservation.status='E'
            reservation.save()



class ReservationList(ListAPIView):
    serializer_class = ReservationSerializer
    pagination_class = PageNumberPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query_set = Reservation.objects.all()
        host_query_set = query_set.filter(host=self.request.user)
        guest_query_set = query_set.filter(guest=self.request.user)
        role = self.request.GET.get('role')
        if role:
            if role.lower() == 'guest':
                query_set=guest_query_set
            elif role.lower() == 'host':
                query_set=host_query_set
            else:
                query_set=host_query_set.union(guest_query_set)
        else:
            query_set=host_query_set.union(guest_query_set)

        for r in query_set:
            update_status(r)

        status = self.request.GET.get('status')
        if status:
            if status.lower() == 'pending':
                query_set = query_set.filter(status='P')
            elif status.lower() == 'denied':
                query_set = query_set.filter(status='D')
            elif status.lower() == 'expired':
                query_set = query_set.filter(status='E')
            elif status.lower() == 'approved':
                query_set = query_set.filter(status='A')                
            elif status.lower() == 'canceled':
                query_set = query_set.filter(status='C')
            elif status.lower() == 'terminated':
                query_set = query_set.filter(status='T')
            elif status.lower() == 'completed':
                query_set = query_set.filter(status='F')     
        
        return query_set

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def reservation_create(request):
    if request.method == 'POST':
        data = request.POST.dict() #property,start,end

        data['status'] = 'P'
        

        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            if request.user == Property.objects.get(pid=data['property']).owner:
                return Response({'details': 'Host cannot book their own property'}, status=400)
            serializer.save(guest=request.user,
                            host=Property.objects.get(pid=data['property']).owner)
            reservation = serializer.instance
            notification= Notification(recipient=reservation.host,reason=reservation.guest,type='R',reservation=reservation)
            notification.save()
            return Response(data=data)
        return Response(serializer.errors, status=400)
    return Response({'details': 'Something went wrong with the request'}, status=400)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def reservation_cancel(request):
    
    if request.method == 'GET':
        data = request.GET.dict() #rid
        try:
            reservation = Reservation.objects.get(rid=data['rid'])
            update_status(reservation)
        except:
            return Response({'details': 'Reservation not found'}, status=404)
        if request.user == reservation.guest:
            if reservation.status == 'P':
                notification= Notification(recipient=reservation.host,reason=reservation.guest,type='N',reservation=None)
                reservation.delete()
                notification.save()
            elif reservation.status == 'A':
                reservation.status = 'C'
                reservation.save()
                notification= Notification(recipient=reservation.host,reason=reservation.guest,type='C',reservation=reservation)
                notification.save()
            else:
                return Response({'details': "Guest can't cancel requests that aren't pending or accepted"}, status=400)
        elif request.user == reservation.host:
            if reservation.status == 'P':
                reservation.status = 'D'
                reservation.save()
                notification= Notification(recipient=reservation.guest,reason=reservation.host,type='D',reservation=reservation)
                notification.save()
            elif reservation.status == 'A':
                reservation.status = 'T'
                reservation.save()
                notification= Notification(recipient=reservation.guest,reason=reservation.host,type='T',reservation=reservation)
                notification.save()
            else:
                return Response({'details': "Host can't cancel reservations that aren't pending or accepted"}, status=400)
        else:
            return Response({'details': "Forbidden, user not host or guest of reservation"}, status=403)
        return Response({'details': 'Cancel successul'}, status=200)
    return Response({'details': 'Something went wrong with the request'}, status=400)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def reservation_approve(request):
   
    if request.method == 'GET':
        data = request.GET.dict() #rid
        try:
            reservation = Reservation.objects.get(rid=data['rid'])
            update_status(reservation)
        except:
            return Response({'details': 'Reservation not found'}, status=404)
        if request.user == reservation.host:
            print(reservation.status)
            if reservation.status == 'P':
                reservation.status = 'A'
                reservation.save()
                notification= Notification(recipient=reservation.guest,reason=reservation.host,type='A',reservation=reservation)
                notification.save()
            else:
                return Response({'details': "Host can't approve reservations that aren't pending"}, status=400)

        else:
            return Response({'details': "Guest can't approve reservations"}, status=400)
        print(reservation.status)
        return Response({'details': 'Approve successul'}, status=200)
    return Response({'details': 'Something went wrong with the request'}, status=400)
