from django.db import models
from django.contrib.auth.models import User

from hardcoded_models.models import PosesList
from hardcoded_models.models import PlacesList


class Location(models.Model):
    user = models.OneToOneField(User)
    latitude = models.DecimalField(max_digits=16, decimal_places=6)
    longitude = models.DecimalField(max_digits=16, decimal_places=6)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class CheckinDetails(models.Model):
    location = models.OneToOneField(Location)
    poses = models.ManyToManyField(PosesList)
    places = models.ManyToManyField(PlacesList)
    rating = models.IntegerField()
    duration = models.IntegerField()
    contraception = models.BooleanField()
    with_who = models.OneToOneField(User, related_name='related user')
