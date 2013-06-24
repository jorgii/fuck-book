from datetime import date

from django.core.management.base import BaseCommand
from notifications.models import TipNotification


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in TipNotification.person:
            this_person_notifications = TipNotification.objects.filter(person=this_person)
            #To do: write an if-else statement for when there are no records in the db
            index = this_person_notifications.count() - 1
            last_entry = this_person_notifications.order_by('date')[index]
            if date.today() - last_entry == TipNotification.notification_period:
                TipNotification.objects.create(
                    person=this_person,
                    notification_period=TipNotification.notification_period,
                    message=TipNotification.message,
                    display=TipNotification.display,
                    date_saved=date.today())
