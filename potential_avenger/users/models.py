from django.db import models
from django.contrib.auth.models import User

from hardcoded_models import PosesList
from hardcoded_models import PlacesList


class Person(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField('Person Name', max_length=255)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.Field.choices(choices=GENDER_CHOICES)
    birth_date = models.DateField()
    city = models.CharField('City', max_length=255, null=True)
    photo = models.FileField(upload_to='profile_photos')


class PersonPreferences(models.Model):
    user = models.OneToOneField(User)
    relation = models.OneToOneField(User)
    preferred_poses = models.OneToManyField(PosesList)
    preferred_places = models.OneToManyField()
