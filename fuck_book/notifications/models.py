import random

from django.db import models

from hardcoded_models.models import TipsList


class NotificationTypes (models.Model):
    name = models.CharField('Notification name', max_length=256)
    description = models.CharField('Notification type description', max_length=256, null=True, blank=True)

class NotificationInstance(models.Model):
    person = models.ForeignKey('persons.Person')
    notification_type = models.ForeignKey('notifications.NotificationTypes')
    message = models.CharField('Notification message', max_length=512)
    datetime_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField('Read:', default=False)
    is_archived = models.BooleanField('Read:', default=False)


@staticmethod
def create_tip_message():
    '''Function that choses random tip
    for each tip notification created.
    '''
    try:
        tip_message = random.choice(TipsList.objects.all())
    except IndexError:
        tip_message = "Sorry, no tips in the database."
    return tip_message
