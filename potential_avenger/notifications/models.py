from django.db import models

from users.models import Person
from hardcoded_models.models import NotificationType


class Notification (models.Model):
    type_of_notification = models.ForeignKey(NotificationType)
    person = models.OneToOneField(Person)
    notification_period = models.IntegerField(default=7)
    message = models.CharField('Notification Message', max_length=255)
    display = models.BooleanField(default=True)
