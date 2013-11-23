from django.core.management.base import BaseCommand

from notifications.models import PeriodicalNotification
from persons.models import Person, PersonalSettings
from notifications.management.commands.send_difference_notification import get_most_recent_notification, time_to_send_notification


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in Person.objects.all():
            this_person_settings = PersonalSettings.objects.get(person=this_person)

            if this_person_settings.display_periodical_notification:
                last_entry = get_most_recent_notification(this_person, PeriodicalNotification)

                if time_to_send_notification(last_entry, this_person_settings.periodical_notification_period):
                    PeriodicalNotification.objects.create(person=this_person)
