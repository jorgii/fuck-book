from django.db import models
from django.contrib.auth.models import User

from hardcoded_models.models import NotificationType


class Notification (models.Model):
    type_of_notification = models.ForeignKey(NotificationType)
    user = models.OneToOneField(User)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
