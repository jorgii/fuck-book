from django.db import models
from django.contrib.auth.models import User

from hardcoded_models.models import PosesList
from hardcoded_models.models import PlacesList


class Person(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField('Person Name', max_length=255)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    city = models.CharField('City', max_length=255, null=True)
    photo = models.FileField(upload_to='profile_photos')


class PersonPreferences(models.Model):
    person = models.OneToOneField(Person)
    relation = models.OneToOneField(User, related_name='related user')
    preferred_poses = models.ManyToManyField(PosesList)
    preferred_places = models.ManyToManyField(PlacesList)


class PersonalSettings(models.Model):
    user = models.OneToOneField(User)
    useful_tips = models.BooleanField()
    notification_period = models.IntegerField()
