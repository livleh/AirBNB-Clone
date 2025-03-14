from django.urls import include, path
from rest_framework import routers
from . import views

app_name="reservation"
urlpatterns = [
    path('reservationlist/', views.ReservationList.as_view(), name='reservationlist'),
    path('reserve/', views.reservation_create, name='reservation_create'),
    path('cancel/', views.reservation_cancel, name='reservation_cancel'),
    path('approve/', views.reservation_approve, name='reservation_approve'),

]