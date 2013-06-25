from datetime import date

from django.core.management.base import BaseCommand
from notifications.models import DifferenceNotification
from users.models import Person, PersonalSettings


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in Person.objects.all():
            same_person = PersonalSettings.objects.get(person=this_person)
            if same_person.display_difference_notification is True:
                this_person_notifications = DifferenceNotification.objects.filter(person=this_person)
                if this_person_notifications.count() == 0:
                    DifferenceNotification.objects.create(
                        person=this_person,
                        message="Wellcome! You will start getting notifications... .")
                else:
                    last_entry = this_person_notifications.latest('date_saved')
                    if (date.today() - last_entry.date_saved).days == same_person.difference_notification_period:
                        DifferenceNotification.objects.create(person=this_person)
