from datetime import date

from django.db import models

from hardcoded_models.models import PosesList, PlacesList
from users.models import Person


class CheckinDetails(models.Model):
    person = models.ForeignKey(Person)
    date_checked = models.DateField(default=date.today())
    address = models.CharField('Address', max_length=255)
    poses = models.ManyToManyField(PosesList)
    places = models.ManyToManyField(PlacesList)
    rating = models.IntegerField(default=3)
    duration = models.IntegerField(default=10)
    contraception = models.BooleanField(default=True)
    with_who = models.ForeignKey(Person, related_name='checkin related user', null=True)
