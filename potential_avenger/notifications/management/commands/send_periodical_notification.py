from datetime import date

from django.core.management.base import BaseCommand
from notifications.models import PeriodicalNotification
from users.models import Person, PersonalSettings


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in Person.objects.all():
            same_person = PersonalSettings.objects.get(person=this_person)
            if same_person.display_periodical_notification is True:
                this_person_notifications = PeriodicalNotification.objects.filter(person=this_person)
                last_entry = this_person_notifications.latest('date_saved')
                if (date.today() - last_entry.date_saved).days == same_person.periodical_notification_period:
                    PeriodicalNotification.objects.create(person=this_person)
