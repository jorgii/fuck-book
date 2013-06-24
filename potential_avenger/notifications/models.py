from datetime import date
from random import randint

from django.db import models

from users.models import Person
from hardcoded_models.models import TipsList


class PeriodicalNotification (models.Model):
    person = models.OneToOneField(Person)
    message = models.CharField(
        'Notification Message',
        max_length=255,
        default="Haven't checked-in in a while. Sex life getting slow?")
    date_saved = models.DateField(default=date.today())


class TipNotification (models.Model):
    person = models.OneToOneField(Person)
    message = models.CharField('Notification Message', max_length=255)
    date_saved = models.DateField(default=date.today())

    def __init__(self, message):
        tips_counter = TipsList.objects.count() - 1
        index_tips = randint(0, tips_counter)
        self.message = TipsList.objects.all()[index_tips]
        return self.message


class DifferenceNotification (models.Model):
    person = models.OneToOneField(Person)
    message = models.CharField('Notification Message', max_length=255)
    date_saved = models.DateField(default=date.today())

    def __init__(self, message):
        self.message = " "  # To do after Diary is ready
        return self.message
