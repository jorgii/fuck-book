from datetime import date
from collections import Counter

from django.core.management.base import BaseCommand

from notifications.models import DifferenceNotification
from users.models import Person, PersonalSettings, PersonPreferences
from checkin.models import CheckinDetails


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in Person.objects.all():
            this_person_settings = PersonalSettings.objects.get(person=this_person)
            this_person_preferences = PersonPreferences.objects.get(person=this_person)
            related_person = this_person_preferences.relation
            if this_person_settings.display_difference_notification and related_person:
                this_person_notifications = DifferenceNotification.objects.filter(person=this_person)
                last_entry = this_person_notifications.latest('date_saved')
                if (date.today() - last_entry.date_saved).days >= this_person_settings.difference_notification_period:
                    # Get a list of all checkins of those two people since the last notification
                    start_date = last_entry.date_saved
                    end_date = date.today()
                    latest_checkins = list(CheckinDetails.objects.filter(person=this_person,
                                                                         with_who=related_person,
                                                                         date_checked__range=(start_date, end_date)))
                    latest_checkins.extend(list(CheckinDetails.objects.filter(person=related_person,
                                                                              with_who=this_person,
                                                                              date_checked__range=(start_date, end_date))))
                    if latest_checkins:
                        # Get a list of all poses and a list of all places since the last notification
                        latest_poses = list()
                        latest_places = list()
                        for checkin in latest_checkins:
                            latest_poses.extend(list(checkin.poses.all()))
                            latest_places.extend(list(checkin.places.all()))
                        # Count how many times each pose is used
                        poses_counter = Counter()
                        for pose in latest_poses:
                            poses_counter[pose] += 1
                        # Count how many times each place is used
                        places_counter = Counter()
                        for place in latest_places:
                            places_counter[place] += 1
                        # Do some calculation magic
                        related_person_preferences = PersonPreferences.objects.get(person=related_person)
                        related_person_preferred_poses = list(related_person_preferences.preferred_poses.all())
                        related_person_preferred_places = list(related_person_preferences.preferred_places.all())
                        related_person_preferred_poses_count = len(related_person_preferred_poses)
                        related_person_preferred_places_count = len(related_person_preferred_places)
                        if related_person_preferred_poses_count and related_person_preferred_places_count:
                            if len(poses_counter) % 2 == 0:
                                n = int(len(poses_counter)/2)
                            else:
                                n = int((len(poses_counter)+1) / 2)
                            if len(places_counter) % 2 == 0:
                                i = int(len(places_counter)/2)
                            else:
                                i = int((len(places_counter)+1) / 2)
                            counterposes = 0
                            counterplaces = 0
                            for preferred_pose in related_person_preferred_poses:
                                if preferred_pose in poses_counter.most_common(n):
                                    counterposes += 1
                            for preferred_place in related_person_preferred_places:
                                if preferred_place in places_counter.most_common(i):
                                    counterplaces += 1
                            # Get the message for the notification
                            poses_index = counterposes/related_person_preferred_poses_count
                            places_index = counterplaces/related_person_preferred_places_count
                            if poses_index <= 1/2 and places_index <= 1/2:
                                difference_message = "Damn, you're selfish! You need to think more about what poses and places your partner likes."
                            elif poses_index <= 1/2 and places_index > 1/2:
                                difference_message = "You're doing good with the places, but you need to think more about what poses your partner likes."
                            elif poses_index > 1/2 and places_index <= 1/2:
                                difference_message = "You're doing good with the poses, but try to spice it up with some places your partner likes."
                            else:
                                difference_message = "Nice to see you care about what your partner likes. Keep up the good 'work'! ;)"
                        else:
                            difference_message = "You're partner hasn't specified his/her preferences yet."
                    else:
                        difference_message = "Not enough data yet. You have to check in more often. ;)"
                    # And finally create the notification
                    DifferenceNotification.objects.create(person=this_person,
                                                          message=difference_message)
