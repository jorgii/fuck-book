from django.db import models
from django.contrib.auth.models import User

from hardcoded_models.models import PosesList
from hardcoded_models.models import PlacesList


class Person(models.Model):
    user = models.OneToOneField(User)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    city = models.CharField('City', max_length=255, null=True)
    photo = models.FileField(upload_to='potential_avenger/media/profile_photos')


class PersonPreferences(models.Model):
    person = models.OneToOneField(Person)
    relation = models.OneToOneField(Person, related_name='related user', null=True)
    preferred_poses = models.ManyToManyField(PosesList)
    preferred_places = models.ManyToManyField(PlacesList)


class PersonalSettings(models.Model):
    person = models.OneToOneField(Person)
    useful_tips = models.BooleanField()
    notification_period = models.IntegerField()
