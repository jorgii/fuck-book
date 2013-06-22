from django.db import models

import datetime
from users.models import Person
from hardcoded_models.models import NotificationType


class Notification (models.Model):
    type_of_notification = models.ForeignKey(NotificationType)
    person = models.OneToOneField(Person)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()

    def save(self):
        if self.date_created is None:
            self.date_created = datetime.now()
        self.date_modified = datetime.now()
        super(Notification, self).save()
