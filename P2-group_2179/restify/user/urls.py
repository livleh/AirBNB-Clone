from django.urls import path
from . import views
from user.views import Register_View, Change_Password_View, Update_Profile_View

app_name = 'user'

urlpatterns = [ 
    path('register/', Register_View.as_view(), name ="register"),
    path('change_password/', views.changepassword, name="change_password" ),
    path('change_profile/', views.changeprofile, name="change_profile" ),
    #path('update_profile/<int:pk>/', Update_Profile_View.as_view(), name='update_profile'),
    path('profile/', views.ProfileDetail.as_view(), name='profile_detail')

#     path('signup/', views.signup.as_view(), name="signup") ,
#     path('signup/', views.signup_create(), name="signup") ,

#     path('<int:pid>/', views.profile_detail, name='property_detail'),

#     path('login/', views.LoginView.as_view(), name="login"),
#     path('logout/', views.logout, name="logout"),
#     path('profile/view/', views.view_profile, name ="profile"),
#     path('profile/edit/',views.edit_profile.as_view(),name='edit'),
]