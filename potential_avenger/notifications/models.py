from django.db import models

from users.models import Person
from hardcoded_models.models import NotificationType


class Notification (models.Model):
    type_of_notification = models.ForeignKey(NotificationType)
    person = models.OneToOneField(Person)
    timestamp = models.DateTimeField(auto_now=True)
