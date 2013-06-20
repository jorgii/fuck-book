from time import time


from django.db import models
from django.contrib.auth.models import User

from hardcoded_models.models import PosesList
from hardcoded_models.models import PlacesList


def get_upload_file_name(instance, filename):
    return 'profile_photos/{}_{}{}'.format(str(time()).replace('.', '_'), instance.user.id, str(filename[filename.rfind('.'):len(filename)]))


class Person(models.Model):
    user = models.OneToOneField(User)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    city = models.CharField('City', max_length=255, blank=True, null=True)
    photo = models.FileField(upload_to=get_upload_file_name, verbose_name="Profile photo")

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class PersonPreferences(models.Model):
    person = models.OneToOneField(Person)
    relation = models.OneToOneField(Person, related_name='related user', blank=True, null=True)
    preferred_poses = models.ManyToManyField(PosesList)
    preferred_places = models.ManyToManyField(PlacesList)

    def __str__(self):
        return self.person.__str__()

    def save(self):
        super().save()

        if self.relation and self.relation.personpreferences.relation != self.person:
            self.relation.personpreferences.relation
            self.relation.personpreferences.save()


class PersonalSettings(models.Model):
    person = models.OneToOneField(Person)
    useful_tips = models.BooleanField(default=False)
    notification_period = models.IntegerField(default=0)

    def __str__(self):
        return self.person.__str__()
