# from django import forms
# from django.shortcuts import render
# from rest_framework.parsers import JSONParser
# from .models import SignUp
# # Create your views here.

# from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import login, authenticate
# from .forms import LogIn_Form, SignUp_Form, Edit_Form
# from django.shortcuts import redirect
# from django.contrib.auth import login as login_user, \
#                                 logout as logout_user
# from django.urls import reverse, reverse_lazy
# from django.views.generic.edit import FormView

# from django.contrib.auth.models import User
# from .serializers import SignUpSerializer
# # Create your views here.
# from django.http import HttpResponse


# @csrf_exempt
# def signup_create(request):
# 	if request.method == 'POST':
# 		data = request.POST.dict()
		
# 		serializer = SignUpSerializer(data=data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return JsonResponse(data=data)

# 	return HttpResponse(status=400)

# @csrf_exempt
# def profile_detail(request, pid):

# 	try:
# 		profile_ = SignUp.objects.get(pid=pid)
# 	except SignUp.DoesNotExist:
# 		return HttpResponse(status=404)

# 	if request.method == 'GET':
# 		serializer = SignUpSerializer(profile_)
# 		return JsonResponse(serializer.data)

# 	elif request.method == 'PUT':
# 		data = JSONParser().parse(request)
# 		serializer = SignUpSerializer(profile_, data=data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return JsonResponse(serializer.data)
# 		return JsonResponse(serializer.errors, status=400)

# 	elif request.method == 'DELETE':
# 		profile_.delete()
# 		return HttpResponse(status=204)


# class signup(FormView):
#     form_class = SignUp_Form
#     template_name = 'user/signup/.html/'
#     success_url = '/user/login/'

#     def form_valid(self, form):
#         user = User.objects.create_user(first_name= form.cleaned_data.get('first_name'),
#                                         last_name= form.cleaned_data.get('last_name'),
#                                         email=form.cleaned_data.get('email'),
#                                         password= form.cleaned_data.get('password1'), 
#                                         phone_number= form.cleaned_data.get('phone_number'),
#                                         last_name= form.cleaned_data.get('last_name'))
#         return super().form_valid(form)

# class LoginView(FormView):
#     form_class = LogIn_Form
#     template_name = 'user/login.html/'
#     success_url = '/user/profile/view/'

#     def form_valid(self, form):
#         login_user(self.request, form.cleaned_data['user'])
#         return super().form_valid(form)

# def logout(request):
#     logout_user(request)
#     return redirect(reverse('accounts:login'))


# def view_profile(request):
#     if request.user.is_authenticated:
#         user = request.user
#         profile_data = {
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "phone_numer": user.phone_number,
#             "email": user.email
#         }
#         return JsonResponse(profile_data)
#     else:
#         return HttpResponse('Unauthorized', status=401)
    

# class edit_profile(UpdateView):
#     template_name = 'user/profile.html'
#     form_class = Edit_Form
#     model=User

#     def get_success_url(self):
#           return reverse_lazy('user:view')

#     def get_object(self, queryset=None):
#         user=self.request.user
#         return user

#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponse('Unauthorized', status=401)
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         user = self.get_object()
#         password1 = form.cleaned_data.get('password1')
#         if password1:
#             user.set_password(password1)
#             print("before auth")
#             update_session_auth_hash(self.request, self.object)
#             print("after auth")
#         user.username=(form.cleaned_data.get('username'))
#         user.email=(form.cleaned_data.get('email'))
#         user.first_name=(form.cleaned_data.get('first_name'))
#         user.last_name=(form.cleaned_data.get('last_name'))
#         user.save()
#         return super().form_valid(form)

from rest_framework import generics

from .serializers import RegisterSerializer, ChangePasswordSerializer, UpdateProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import uuid
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

class Register_View(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                            "RequestId": str(uuid.uuid4()),
                            "Message": "User created",
                            
                            "User": serializer.data}
                             )
    
        return Response ("Error")
        # serializer.is_valid(raise_exception = True)
        # serializer.save()

        #return Response({"User": serializer.data})

class Change_Password_View(generics.UpdateAPIView):
    #queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                            "RequestId": str(uuid.uuid4()),
                            "Message": "Changed Password Successfully",
                            
                            "User": serializer.data}
                             )
    
        return Response ("Error")
        
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def changepassword(request):

    if request.method == 'PUT':
        user = request.user
        data = request.data
        user_ = User.objects.get(username=user)
        print(user_)

        print(user_.check_password(request.data['old_password']))
        if user_.check_password(request.data['old_password']) is False:
            return Response({'error': 'old password does not match'}, status=400)
        
        # validate that pw and re-entry of pw are same
        if request.data['password'] != request.data['password1']:
            return Response({'error': 'new passwords do not match eachother'}, status=400)
        
        user_.set_password(request.data['password'])
        user_.save()
        return Response({'message': 'successfully changed password'}, status=200)

    return Response({'details': 'Something went wrong with the request'}, status=400)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def changeprofile(request):

    if request.method == 'PUT':
        user = request.user
        data = request.data
        user_ = User.objects.get(username=user)
        
        # check which data is being sent to change
        if request.data == None:
            return Response({'error': 'no information sent to be updated'})
        
        if "email" in request.data:
            user_.email = request.data["email"]

        if "first_name" in request.data:
            user_.first_name = request.data["first_name"]
            
        if "last_name" in request.data:
            user_.last_name = request.data["last_name"]

        user_.save()
        return Response({'message':'successfuly updated profile'}, status=200)

    return Response({'details': 'Something went wrong with the request'}, status=400)

class Update_Profile_View(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateProfileSerializer


class ProfileDetail(generics.RetrieveAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get_object(self):
        return self.request.user