from django.urls import include, path
from rest_framework import routers
from . import views

app_name="property"
urlpatterns = [
    path('', views.PropertyList.as_view(), name='property_list'),
    path('<int:pid>/', views.property_detail, name='property_detail'),
    path('create/', views.property_create, name='property_create'),
    path('<int:pid>/images/add/', views.image_add, name='image_add'),
    path('<int:pid>/images/', views.PropertyImages.as_view(), name='property_images'),
    path('images/<int:image_id>/delete/', views.image_delete, name='image_delete'),
]