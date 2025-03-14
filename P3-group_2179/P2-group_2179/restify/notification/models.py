from django.db import models
from django.contrib.auth.models import User
from reservation.models import Reservation


class Notification(models.Model):
    type_choices= (
        ('N', 'Deleted'), #User deleted a pending reservation
        ('C', 'Canceled'), #User canceled an approved reservation
        ('D', 'Denied'), # Host denied pending reservation
        ('T', 'Terminated'), # Host terminated accepted reservation
        ('A', 'Approved'), # host approved a pending reservation
        ('R', 'Reserved') # guest made a reservation
    )
    nid = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recipient_notifications')
    reason = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reason_notifications')
    type = models.CharField(max_length=1,choices=type_choices)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True)


