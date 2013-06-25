from datetime import date

from django.core.management.base import BaseCommand
from notifications.models import TipNotification
from users.models import Person, PersonalSettings


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in Person.objects.all():
            same_person = PersonalSettings.objects.get(person=this_person)
            if same_person.display_tip_notification is True:
                this_person_notifications = TipNotification.objects.filter(person=this_person)
                if this_person_notifications.count() == 0:
                    TipNotification.objects.create(
                        person=this_person,
                        message="Wellcome! You will start getting notifications... .")
                else:
                    last_entry = this_person_notifications.latest('date_saved')
                    if (date.today() - last_entry.date_saved).days == same_person.tip_notification_period:
                        TipNotification.objects.create(person=this_person)
