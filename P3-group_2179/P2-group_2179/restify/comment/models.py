from django.db import models
from django.contrib.auth.models import User
from property.models import Property
from reservation.models import Reservation

# Create your models here.
class PropertyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=600)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='replies', default=None)
    date = models.DateTimeField(auto_now_add=True)
    reservation = models.ForeignKey(Reservation, null=True, on_delete=models.SET_NULL, default=None)


class UserComment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=600)
    date = models.DateTimeField(auto_now=True)