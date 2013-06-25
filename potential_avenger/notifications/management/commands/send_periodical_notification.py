from datetime import date

from django.core.management.base import BaseCommand
from notifications.models import PeriodicalNotification
from users.models import PersonalSettings


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in PeriodicalNotification.person:
            same_person = PersonalSettings.objects.get(person=this_person)
            if same_person.display_periodical_notification is True:
                this_person_notifications = PeriodicalNotification.objects.filter(person=this_person)
                if this_person_notifications.count() == 0:
                    PeriodicalNotification.objects.create(
                        person=this_person,
                        message="Wellcome! Don't hesitate to make your first check in.")
                else:
                    last_entry = this_person_notifications.latest('date_saved')
                    if date.today() - last_entry.date_saved == same_person.periodical_notification_period:
                        PeriodicalNotification.objects.create(person=this_person)
