from datetime import date
from collections import Counter
from decimal import Decimal

from django.core.management.base import BaseCommand

from notifications.models import DifferenceNotification
from persons.models import Person, PersonalSettings, PersonPreferences
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
                        difference_message = self.DIFFERENCE_MESSAGE['no_checkins']
                    else:
                        latest_poses = self.get_latest_items("poses", latest_checkins)
                        latest_places = self.get_latest_items("places", latest_checkins)

                        if not latest_poses or not latest_places:
                            difference_message = self.DIFFERENCE_MESSAGE['no_poses_or_paces']
                        else:
                            poses_counter = self.get_items_usage(latest_poses)
                            places_counter = self.get_items_usage(latest_places)

                            related_person_preferences = PersonPreferences.objects.get(person=related_person)
                            related_person_preferred_poses = list(related_person_preferences.preferred_poses.all())
                            related_person_preferred_places = list(related_person_preferences.preferred_places.all())
                            related_person_preferred_poses_count = len(related_person_preferred_poses)
                            related_person_preferred_places_count = len(related_person_preferred_places)

                            if related_person_preferred_poses_count == 0 or related_person_preferred_places_count == 0:
                                difference_message = self.DIFFERENCE_MESSAGE['no_preferred_poses_or_places']
                            else:
                                difference_message = self.get_difference_message(poses_counter,
                                                                                 places_counter,
                                                                                 related_person_preferred_poses,
                                                                                 related_person_preferred_places,
                                                                                 related_person_preferred_poses_count,
                                                                                 related_person_preferred_places_count)

                    DifferenceNotification.objects.create(person=this_person,
                                                          message=difference_message)

    INDEX_CONSTANT = Decimal(1)/Decimal(2)
    DIFFERENCE_MESSAGE = {'no_checkins': "Not enough data yet. You have to check in more often. ;)",
                          'no_poses_or_paces': "If you want to get these, you have to specify poses and places when you checkin.",
                          'no_preferred_poses_or_places': "Your partner hasn't specified all of his/her preferences yet.",
                          'places_enough': "You're doing good with the places, but you need to think more about what poses your partner likes.",
                          'poses_enough': "You're doing good with the poses, but try to spice it up with some places your partner likes.",
                          'both_enough': "Nice to see you care about what your partner likes. Keep up the good 'work'! ;)",
                          'both_not_enough': "Damn, you're selfish! You need to think more about what poses and places your partner likes."}

    def get_couple_latest_checkins(self, person1, person2, last_notification):
        ''' Takes three parameters - a person, his related person and the last difference
        notification the person got.
        Returns a list of all checkins made by the couple since that last notification.
        '''
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
        ''' Takes:
        - item - can be either "poses" or "paces"
        - checkins - the list of all checkins made by the couple since the last notification.
        Depending on the value of item returns either a list of all poses or places used in those checkins.
        '''
        latest_items = list()
        if item == "poses":
            for checkin in checkins:
                latest_items.extend(list(checkin.poses.all()))
        elif item == "places":
            for checkin in checkins:
                latest_items.extend(list(checkin.places.all()))
        return latest_items

    def get_items_usage(self, items_list):
        ''' Takes one parameter - either a list of poses or a list of places,
        used in couple's checkins.
        Returns a Counter object, which contains how many times each item is used.
        '''
        items_counter = Counter()
        for item in items_list:
            items_counter[item] += 1
        return items_counter

    def get_difference_message(self, items_counter1, items_counter2, preferred_items1, preferred_items2, preferred_items_count1, preferred_items_count2):
        ''' Takes:
        - items_counter1 - a Counter object of the poses used in copule's checkins
        - items_counter2 - a Counter object of the places used in copule's checkins
        - preferred_items1 - a list of related person preferred poses
        - preferred_items2 - a list of related person preferred places
        - preferred_items_count1 - the number of related person preferred poses
        - preferred_items_count2 - the number of related person preferred places
        Returns the notification message according to how many times a preferred item
        was found in the Counter object's most common half.
        '''
        poses_half = self.calculate_half_of_used_items(items_counter1)
        places_half = self.calculate_half_of_used_items(items_counter2)

        matching_poses = self.count_matching_items(preferred_items1, items_counter1, poses_half)
        matching_places = self.count_matching_items(preferred_items2, items_counter2, places_half)

        poses_index = Decimal(matching_poses)/Decimal(preferred_items_count1)
        places_index = Decimal(matching_places)/Decimal(preferred_items_count2)

        if poses_index <= self.INDEX_CONSTANT and places_index <= self.INDEX_CONSTANT:
            message = self.DIFFERENCE_MESSAGE['both_not_enough']
        elif poses_index <= self.INDEX_CONSTANT and places_index > self.INDEX_CONSTANT:
            message = self.DIFFERENCE_MESSAGE['places_enough']
        elif poses_index > self.INDEX_CONSTANT and places_index <= self.INDEX_CONSTANT:
            message = self.DIFFERENCE_MESSAGE['poses_enough']
        else:
            message = self.DIFFERENCE_MESSAGE['both_enough']
        return message

    def calculate_half_of_used_items(self, items_counter):
        ''' Takes one parameter - a Counter object, which contains how many times each item is used.
        Returns an integer number, which is the middle of the Counter object.
        '''
        if len(items_counter) % 2 == 0:
            half = int(len(items_counter)/2)
        else:
            half = int((len(items_counter)+1)/2)
        return half

    def count_matching_items(self, preferred_items, items_counter, half):
        ''' Takes:
        - preferred_items - a list of related person preferred poses or places
        - items_counter - a Counter object, which contains how many times each item is used in couple's checkins
        - half - an integer number, which is the middle of the Counter object.
        Returns a number, which equals the times an item from preferred_items matched an item
        in the Counter object's most common half.
        '''
        counter = 0
        list_of_items = [x[0] for x in items_counter.most_common(half)]
        for item in preferred_items:
            if item in list_of_items:
                counter += 1
        return counter


def get_most_recent_notification(person, cls):
    ''' Takes two parameters - person and notification class.
    Returns the last notification this person got from the given type.
    '''
    this_person_notifications = cls.objects.filter(person=person)
    return this_person_notifications.latest('date_saved')


def time_to_send_notification(last_notification, notification_period_settings):
    ''' Takes:
    - last_notification - the last notification person got from a given type
    - notification_period_setting - the period in which a notifications should be sent to this same person.
    Returns True if it's time to send new notification.
    '''
    return (date.today() - last_notification.date_saved).days >= notification_period_settings
