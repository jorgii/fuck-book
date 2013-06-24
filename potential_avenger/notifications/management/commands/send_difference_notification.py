from datetime import date

from django.core.management.base import BaseCommand
from notifications.models import DifferenceNotification


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in DifferenceNotification.person:
            # To do: add if-else statement that checks if the person wants notifications
            this_person_notifications = DifferenceNotification.objects.filter(person=this_person)
            if this_person_notifications.count() == 0:
                pass  # To do: add action for when there are no entries in the DB
            else:
                last_entry = this_person_notifications.latest('date_saved')
                if date.today() - last_entry.date_saved == DifferenceNotification.notification_period:
                    DifferenceNotification.objects.create(
                        person=this_person,
                        notification_period=last_entry.notification_period,
                        message=last_entry.message,
                        display=last_entry.display,
                        date_saved=date.today())
