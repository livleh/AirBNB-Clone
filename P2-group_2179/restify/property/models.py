from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# https://piazza.com/class/lcfnmas0pjs2sw/post/807
# Don't need the availability
class Property(models.Model):
  pid = models.AutoField(primary_key=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  price = models.PositiveIntegerField()
  rating = models.FloatField(default=0)
  num_ratings = models.PositiveIntegerField(default=0)
  image_counter = models.PositiveIntegerField(default=0)

  # Property features
  num_guests = models.PositiveIntegerField()
  num_beds = models.PositiveIntegerField()
  num_baths = models.PositiveIntegerField()
  wifi = models.BooleanField(default=False)
  kitchen = models.BooleanField(default=False)
  tv = models.BooleanField(default=False)
  air_con = models.BooleanField(default=False)
  pool = models.BooleanField(default=False)
  barbecue = models.BooleanField(default=False)
  free_parking = models.BooleanField(default=False)


# https://medium.com/ibisdev/upload-multiple-images-to-a-model-with-django-fd00d8551a1c
# For multiple images
class Image(models.Model):
  name = models.CharField(max_length=255)
  image_property = models.ForeignKey(Property, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='images/')
  default = models.BooleanField(default=False)