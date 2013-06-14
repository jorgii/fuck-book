from django.db import models

from hardcoded_models.models import PosesList
from hardcoded_models.models import PlacesList


class Location(models.Model):
    person = models.OneToOneField('users.Person')
    latitude = models.DecimalField(max_digits=16, decimal_places=6)
    longitude = models.DecimalField(max_digits=16, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)


class CheckinDetails(models.Model):
    location = models.OneToOneField(Location)
    poses = models.ManyToManyField(PosesList)
    places = models.ManyToManyField(PlacesList)
    rating = models.IntegerField()
    duration = models.IntegerField()
    contraception = models.BooleanField()
    with_who = models.OneToOneField('users.Person', related_name='checkin related user', null=True)
