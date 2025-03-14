from django.db import models
from django.contrib.auth.models import User
from property.models import Property
from datetime import date

class Reservation(models.Model):
    status_choices= (
        ('P', 'Pending'), #makes request
        ('D', 'Denied'), # host denied
        ('E', 'Expired'), # host didnt respond after x days
        ('A', 'Approved'), # host approved
        ('C', 'Canceled'), # host approved but user canceled
        ('T', 'Terminated'), #host approved but host canceled
        ('F', 'Completed') # stay successful
    )
    rid = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='host_reservations')
    guest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='guest_reservations')
    start = models.DateField()
    end = models.DateField()
    status = models.CharField(max_length=1,choices=status_choices)
    created = models.DateField(auto_now_add=True)
