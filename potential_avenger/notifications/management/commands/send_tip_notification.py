from datetime import date

from django.core.management.base import BaseCommand
from notifications.models import TipNotification
from users.models import PersonalSettings


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in TipNotification.person:
            for same_person in PersonalSettings:
                if this_person == same_person.person and same_person.display_tip_notification is True:
                    this_person_notifications = TipNotification.objects.filter(person=this_person)
                    if this_person_notifications.count() == 0:
                        pass  # To do: add action for when there are no entries in the DB
                    else:
                        last_entry = this_person_notifications.latest('date_saved')
                        if date.today() - last_entry.date_saved == same_person.tip_notification_period:
                            TipNotification.objects.create(
                                person=this_person,
                                message=last_entry.message,
                                date_saved=date.today())
                else:
                    pass
