from datetime import date
from random import randint

from django.db import models

from users.models import Person
from hardcoded_models.models import TipsList


class PeriodicalNotification (models.Model):
    person = models.ForeignKey(Person)
    message = models.CharField(
        'Notification Message',
        max_length=255,
        default="Haven't checked-in in a while. Sex life getting slow?")
    date_saved = models.DateField(default=date.today())


def create_tip_message():
    tips_counter = TipsList.objects.count() - 1
    index_tips = randint(0, tips_counter)
    tip_message = TipsList.objects.all()[index_tips]
    return tip_message


class TipNotification (models.Model):
    person = models.ForeignKey(Person)
    message = models.CharField('Notification Message', max_length=255, default=create_tip_message)
    date_saved = models.DateField(default=date.today())


def create_difference_message():
    difference_message = "."  # To do after Diary is ready
    return difference_message


class DifferenceNotification (models.Model):
    person = models.ForeignKey(Person)
    message = models.CharField('Notification Message', max_length=255, default=create_difference_message)
    date_saved = models.DateField(default=date.today())
