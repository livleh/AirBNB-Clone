import datetime
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .serializers import PropertyCommentSerializer, UserCommentSerializer
from .models import PropertyComment, UserComment
from property.models import Property
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt # Need to remove this line when validation is proper
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from reservation.models import Reservation
from django.contrib.auth.models import User

# Create your views here.
class PropertyCommentList(ListAPIView):
  serializer_class = PropertyCommentSerializer
  pagination_class = PageNumberPagination

  def get_queryset(self):
      pid = self.kwargs['pid']
      queryset = PropertyComment.objects.filter(comment_property__pid=pid).order_by('date')
      return queryset

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def property_comment_reply(request, pid, cid):
  try:
    property_ = Property.objects.get(pid=pid)
  except Property.DoesNotExist:
    return Response({'details': 'Property not found'}, status=404)
  
  try:
    parent_comment = PropertyComment.objects.get(pk=cid)
  except PropertyComment.DoesNotExist:
    return Response({'details': 'Parent comment not found'}, status=404)
  
  if request.method == 'POST':
    data = request.POST.dict()
    user = request.user
    serializer = PropertyCommentSerializer(data=data)
    if serializer.is_valid():
      # User is not the parent comment or the owner
      if user != parent_comment.user and user != property_.owner:
        return Response({'details': 'Cannot comment on this thread at this time'}, status=403)
      comment_thread = PropertyComment.objects.filter(parent__pk=cid).order_by('-date')
      if comment_thread.count() <= 0:
        if user == property_.owner:
          comment = serializer.save(comment_property=property_, user=request.user)
          return Response(data=serializer.data)
        else:
          return Response({'details': 'Cannot comment on this thread at this time'}, status=403)

      else:
        last_user = comment_thread[0].user
        if last_user == user:
          return Response({'details': 'Cannot comment on this thread at this time'}, status=403)
        else:
          comment = serializer.save(comment_property=property_, user=request.user)
          return Response(data=serializer.data)
      # Probably need a check that they have had a reservation before
    else:
      return Response(serializer.errors, status=400)
  
  return Response({'details': 'Something went wrong with the request'}, status=400)



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def property_comment_add(request, pid):
  try:
    property_ = Property.objects.get(pid=pid)
  except Property.DoesNotExist:
    return Response({'details': 'Property not found'}, status=404)

  if request.method == 'POST':
    data = request.POST.dict()
    user = request.user
    serializer = PropertyCommentSerializer(data=data)
    if serializer.is_valid():
      if request.user == property_.owner:
        return Response({'details': 'Cannot start a comment thread on owned property'}, status=403)
      query_set = Reservation.objects.filter(guest=user)
      query_set = query_set.filter(property=property_).order_by('end')

      # Need to check that they had a reservation at all 
      comment = serializer.save(comment_property=property_, user=request.user)
      return Response(data=serializer.data)
    else:
      return Response(serializer.errors, status=400)



  return Response({'details': 'Something went wrong with the request'}, status=400)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_comment_add(request, uid):
  try:
    user = User.objects.get(pk=uid)
  except User.DoesNotExist:
    return Response({'details': 'User not found'}, status=404)
  
  if request.method == 'POST':
      data = request.POST.dict()
      serializer = UserCommentSerializer(data=data)
      if serializer.is_valid():
        if request.user == user:
          return Response({'details': 'Cannot comment on self'}, status=403)
        
        query_set = Reservation.objects.filter(host=request.user)
        query_set = query_set.filter(guest=user)
        query_set = query_set.filter(status='F')
        now = datetime.datetime.now()
        query_set = query_set.filter(end__lt=now)
        if query_set.count() <= 0:
          return Response({'details': 'Cannot comment on this user'}, status=403)
        
        query_set = UserComment.objects.filter(comment_user=request.user)
        query_set = UserComment.objects.filter(user=user)
        if query_set.count() <= 0:
          return Response({'details': 'Already commented on this user'}, status=403)
        serializer.save(comment_user=request.user, user=user)
      else:
        return Response(serializer.errors, status=400)

  return Response({'details': 'Something went wrong with the request'}, status=400)


class UserCommentList(ListAPIView):
  serializer_class = UserCommentSerializer
  pagination_class = PageNumberPagination

  def get_queryset(self):
      uid = self.kwargs['uid']
      queryset = UserComment.objects.filter(user__id=uid).order_by('date')
      return queryset
