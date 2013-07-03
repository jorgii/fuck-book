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
                last_entry = get_most_recent_notification(this_person, DifferenceNotification)

                if time_to_send_notification(last_entry, this_person_settings.difference_notification_period):
                    latest_checkins = self.get_couple_latest_checkins(this_person, related_person, last_entry)

                    if not latest_checkins:
                        difference_message = "Not enough data yet. You have to check in more often. ;)"
                    else:
                        latest_poses = self.get_latest_items("poses", latest_checkins)
                        latest_places = self.get_latest_items("places", latest_checkins)

                        if not latest_poses or not latest_places:
                            difference_message = "If you want to get these, you have to specify poses and places when you checkin."
                        else:
                            poses_counter = self.get_items_usage(latest_poses)
                            places_counter = self.get_items_usage(latest_places)

                            related_person_preferences = PersonPreferences.objects.get(person=related_person)
                            related_person_preferred_poses = list(related_person_preferences.preferred_poses.all())
                            related_person_preferred_places = list(related_person_preferences.preferred_places.all())
                            related_person_preferred_poses_count = len(related_person_preferred_poses)
                            related_person_preferred_places_count = len(related_person_preferred_places)

                            if related_person_preferred_poses_count == 0 or related_person_preferred_places_count == 0:
                                difference_message = "Your partner hasn't specified all of his/her preferences yet."
                            else:
                                difference_message = self.get_difference_message(poses_counter,
                                                                                 places_counter,
                                                                                 related_person_preferred_poses,
                                                                                 related_person_preferred_places,
                                                                                 related_person_preferred_poses_count,
                                                                                 related_person_preferred_places_count)

                    DifferenceNotification.objects.create(person=this_person,
                                                          message=difference_message)

    def get_couple_latest_checkins(self, person1, person2, last_notification):
        start_date = last_notification.date_saved
        end_date = date.today()
        checkins = list(CheckinDetails.objects.filter(person=person1,
                                                      with_who=person2,
                                                      date_checked__range=(start_date, end_date)))
        checkins.extend(list(CheckinDetails.objects.filter(person=person2,
                                                           with_who=person1,
                                                           date_checked__range=(start_date, end_date))))
        return checkins

    def get_latest_items(self, item, checkins):
        latest_items = list()
        if item == "poses":
            for checkin in checkins:
                latest_items.extend(list(checkin.poses.all()))
        elif item == "places":
            for checkin in checkins:
                latest_items.extend(list(checkin.places.all()))
        return latest_items

    def get_items_usage(self, items_list):
        items_counter = Counter()
        for item in items_list:
            items_counter[item] += 1
        return items_counter

    def get_difference_message(self, items_counter1, items_counter2, preferred_items1, preferred_items2, preferred_items_count1, preferred_items_count2):
        poses_half = self.calculate_half_of_used_items(items_counter1)
        places_half = self.calculate_half_of_used_items(items_counter2)

        matching_poses = self.count_matching_items(preferred_items1, items_counter1, poses_half)
        matching_places = self.count_matching_items(preferred_items2, items_counter2, places_half)

        poses_index = matching_poses/preferred_items_count1
        places_index = matching_places/preferred_items_count2

        if poses_index <= 1/2 and places_index <= 1/2:
            message = "Damn, you're selfish! You need to think more about what poses and places your partner likes."
        elif poses_index <= 1/2 and places_index > 1/2:
            message = "You're doing good with the places, but you need to think more about what poses your partner likes."
        elif poses_index > 1/2 and places_index <= 1/2:
            message = "You're doing good with the poses, but try to spice it up with some places your partner likes."
        else:
            message = "Nice to see you care about what your partner likes. Keep up the good 'work'! ;)"
        return message

    def calculate_half_of_used_items(self, items_counter):
            if len(items_counter) % 2 == 0:
                half = int(len(items_counter)/2)
            else:
                half = int((len(items_counter)+1)/2)
            return half

    def count_matching_items(self, preferred_items, items_counter, half):
            counter = 0
            for item in preferred_items:
                if item in items_counter.most_common(half):
                    counter += 1
            return counter


def get_most_recent_notification(person, cls):
    this_person_notifications = cls.objects.filter(person=person)
    return this_person_notifications.latest('date_saved')


def time_to_send_notification(last_notification, notification_period_settings):
    return (date.today() - last_notification.date_saved).days >= notification_period_settings
