from django.urls import include, path
from rest_framework import routers
from . import views

app_name="notification"
urlpatterns = [
    path('list/', views.NotificationList.as_view(), name='notificationlist'),
    path('<int:nid>/', views.notification_detail, name='notification_detail'),
]