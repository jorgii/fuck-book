from datetime import date

from django.core.management.base import BaseCommand
from notifications.models import DifferenceNotification


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in DifferenceNotification.person:
            this_person_notifications = DifferenceNotification.objects.filter(person=this_person)
            #To do: write an if-else statement for when there are no records in the db
            index = this_person_notifications.count() - 1
            last_entry = this_person_notifications.order_by('date')[index]
            if date.today() - last_entry == DifferenceNotification.notification_period:
                DifferenceNotification.objects.create(
                    person=this_person,
                    notification_period=DifferenceNotification.notification_period,
                    message=DifferenceNotification.message,
                    display=DifferenceNotification.display,
                    date_saved=date.today())
