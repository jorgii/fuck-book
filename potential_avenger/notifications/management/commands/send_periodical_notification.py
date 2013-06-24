from datetime import date

from django.core.management.base import BaseCommand
from notifications.models import PeriodicalNotification


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in PeriodicalNotification.person:
            this_person_notifications = PeriodicalNotification.objects.filter(person=this_person)
            #To do: write an if-else statement for when there are no records in the db
            index = this_person_notifications.count() - 1
            last_entry = this_person_notifications.order_by('date')[index]
            if date.today() - last_entry == PeriodicalNotification.notification_period:
                PeriodicalNotification.objects.create(
                    person=this_person,
                    notification_period=PeriodicalNotification.notification_period,
                    message=PeriodicalNotification.message,
                    display=PeriodicalNotification.display,
                    date_saved=date.today())
