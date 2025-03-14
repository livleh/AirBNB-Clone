from django import forms
from django.contrib.auth import models, authenticate

#Need a form for register, login, logout 
 
#For a register form we need: 
# username, password1, password2, email, first_name, last_name 
# username, password and repeat password are required

# class SignUp_Form(forms.Form):
#     first_name = forms.CharField(required=True, max_length=200)
#     last_name = forms.CharField(required=True, max_length=200)
#     password1 = forms.CharField(widget=forms.PasswordInput(), max_length=200, required=True)
#     password2 = forms.CharField(widget=forms.PasswordInput(), max_length=200, required=True)
#     email = forms.EmailField(required=True, max_length=200)
#     phone_number = forms.IntegerField(required = True)

#     #for validation
#     def clean(self):
#         data = super().clean()

#         password_one = data.get('password1')
#         password_two = data.get('password2')

#         if (password_one != password_two):
#             raise forms.ValidationError({
#                 'password2' : "The two password fields didn't match"}
#             )
        
#         return data
    

# #For a login form we need: 
# # username, password
  
# class LogIn_Form(forms.Form):
#     email = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput())

#     def clean(self):
#         data = super().clean()

#         email = data.get('email')
#         password_one = data.get('password')
#         user = authenticate(username=email, password=password_one)
#         if user:
#             data['user'] = user
#             return data
    
#         raise forms.ValidationError({
#                 'username' : 'Passwrod of Email is invalid!'}
#         )

# class Edit_Form(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput,required=False)
#     password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput,required=False)
#     class Meta:
#         model = User
#         template_name = "accounts/register.html"
#         fields = ["username","email","first_name","last_name"]
#         help_texts = {
#             'username': None,
#         }
#         error_messages = {
#             'username' : {
#                 'unique' : "A user with that username already exists",
#                 'required' : "This field is required",
#             },
#             'email' : {
#                 'invalid' : "Enter a valid email address",
#             },
#         }

#     def clean(self):
#         errors={}
#         data = super().clean()
#         password1=data.get('password1')   
#         password2=data.get('password2')
#         print(password1)

#         if ((len(password1) !=0) and (len(password1)<8)):
#             errors['password1']= "This password is too short. It must contain at least 8 characters"
#             #raise forms.ValidationError({'password1':"This password is too short. It must contain at least 8 characters"})

#         if ((len(password1) !=0) and(password1 != password2)):
#             errors['password2'] = "The two password fields didn't match"
#             #raise forms.ValidationError({'password2':"The two password fields didn't match"})

#         if errors:
#             raise forms.ValidationError(errors)

#         return data
