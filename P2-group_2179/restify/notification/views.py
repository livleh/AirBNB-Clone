from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from reservation.models import Reservation
from .models import Notification
from django.views.decorators.csrf import csrf_exempt # Need to remove this line when validation is proper
from django.http import HttpResponse, JsonResponse
from property.models import Property
from datetime import date,timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import NotificationSerializer

# Create your views here.
class NotificationList(ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = PageNumberPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query_set = Notification.objects.all()
        query_set = query_set.filter(recipient=self.request.user)
        return query_set
    
@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def notification_detail(request,nid):
    try:
        notification_ = Notification.objects.get(nid=nid)
    except:
        return Response({'details': 'Notification not found'}, status=404)
    if request.method == 'GET':
        if request.user != notification_.recipient:
            return Response({'details': 'Forbidden from viewing this notification'}, status=403)
        serializer = NotificationSerializer(notification_)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if request.user != notification_.recipient:
            return Response({'details': 'Forbidden from deleting this notification'}, status=403)
        notification_.delete()
        return Response({'details': 'Notification was deleted'}, status=200)
    return Response({'details': 'Something went wrong with the request'}, status=400)