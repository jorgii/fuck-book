import random
from datetime import date

from django.db import models

from hardcoded_models.models import TipsList


class PeriodicalNotification (models.Model):
    person = models.ForeignKey('users.Person')
    message = models.CharField('Notification Message',
                               max_length=255,
                               default="Haven't checked-in in a while. Sex life getting slow?")
    date_saved = models.DateField(default=date.today())
    unread = models.BooleanField(default=True)

    def __str__(self):
        return '{}, {}'.format(self.date_saved, self.person.user)


def create_tip_message():
    '''Function that choses random tip
    for each tip notification created.
    '''
    try:
        tip_message = random.choice(TipsList.objects.all())
    except IndexError:
        tip_message = "Sorry, no tips in the database."
    return tip_message


class TipNotification (models.Model):
    person = models.ForeignKey('users.Person')
    message = models.CharField('Notification Message', max_length=255, default=create_tip_message)
    date_saved = models.DateField(default=date.today())
    unread = models.BooleanField(default=True)

    def __str__(self):
        return '{}, {}'.format(self.date_saved, self.person.user)


class DifferenceNotification (models.Model):
    person = models.ForeignKey('users.Person')
    message = models.CharField('Notification Message', max_length=255, default=" ")
    date_saved = models.DateField(default=date.today())
    unread = models.BooleanField(default=True)

    def __str__(self):
        return '{}, {}'.format(self.date_saved, self.person.user)
