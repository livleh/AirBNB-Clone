from django.urls import include, path
from rest_framework import routers
from . import views

app_name="comment"
urlpatterns = [
    path('property/<int:pid>/', views.PropertyCommentList.as_view(), name='property_comment_list'),
    path('property/<int:pid>/add/', views.property_comment_add, name='property_comment_add'),
    path('property/<int:pid>/reply/<int:cid>/', views.property_comment_reply, name='property_comment_reply'),
    path('user/<int:uid>/', views.UserCommentList.as_view(), name='user_comment_list'),
    path('user/<int:uid>/add/', views.user_comment_add, name='user_comment_add')
]

