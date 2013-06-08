from django.db import models
from django.contrib.auth.models import User


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
