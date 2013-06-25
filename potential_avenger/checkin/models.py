from datetime import date

from django.db import models

from hardcoded_models.models import PosesList, PlacesList
from users.models import Person


class CheckinDetails(models.Model):
    person = models.OneToOneField(Person)
    date_checked = models.DateField(default=date.today())
    address = models.CharField('Address', max_length=255)
    poses = models.ManyToManyField(PosesList)
    places = models.ManyToManyField(PlacesList)
    rating = models.IntegerField()
    duration = models.IntegerField()
    contraception = models.BooleanField()
    with_who = models.OneToOneField(Person, related_name='checkin related user', null=True)
