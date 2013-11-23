import logging
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError


from notifications.models import PeriodicalNotification, TipNotification, DifferenceNotification
from persons.models import Person, PersonPreferences, PersonalSettings
from hardcoded_models.models import PosesList, TipsList, PlacesList


POSES_LIST = ['advanced_sex', 'leg_lock', 'missionary', 'side_sex', 'spider_web', 'the_mermaid', 'water_sex']
PLACES_LIST = ['bathtub', 'chair', 'desk', 'double_bed', 'table']
TIPS_LIST = ['Tip 1',
             'Tip 2',
             'Tip 3',
             'Tip 4',
             'Tip 5',
             'Tip 6',
             'Tip 7',
             'Tip 8',
             'Tip 9',
             'Tip 10',
             'Tip 11',
             'Tip 12',
             'Tip 13',
             'Tip 14',
             'Tip 15',
             'Tip 16']
USER_DATA = [['user1', 'pass1', 'User1Name1', 'User1Name2'],
             ['user2', 'pass2', 'User2Name1', 'User2Name2'],
             ['user3', 'pass3', 'User3Name1', 'User3Name2'],
             ['user4', 'pass4', 'User4Name1', 'User4Name2'],
             ['user5', 'pass5', 'User5Name1', 'User5Name2'],
             ['user6', 'pass6', 'User6Name1', 'User6Name2'],
             ['user7', 'pass7', 'User7Name1', 'User7Name2']]
PERSON_DATA = [['user1', 'M', '1990-01-25', 'Sofia1'],
               ['user2', 'F', '1991-02-25', 'Sofia2'],
               ['user3', 'F', '1992-03-25', 'Sofia3'],
               ['user4', 'M', '1993-04-25', 'Sofia4'],
               ['user5', 'F', '1994-05-25', 'Sofia5'],
               ['user6', 'M', '1995-06-25', 'Sofia6'],
               ['user7', 'F', '1996-07-25', 'Sofia7']]


class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        logging.info('Start database population.')
        logging.info('Adding hardcoded POSES.')
        for pose in POSES_LIST:
            created_pose = PosesList.objects.create(pose=pose)
            created_pose.save()
        logging.info('Hardcoded POSES added.')
        logging.info('Adding hardcoded PLACES.')
        for place in PLACES_LIST:
            created_place = PlacesList.objects.create(place=place)
            created_place.save()
        logging.info('Hardcoded PLACES added.')
        logging.info('Adding hardcoded TIPS.')
        for tip in TIPS_LIST:
            created_tip = TipsList.objects.create(useful_tip=tip)
            created_tip.save()
        logging.info('Hardcoded TIPS added.')
        logging.info('Creating USERS.')
        for user in USER_DATA:
            try:
                created_user = self.create_user(*user)
                created_user.save()
            except IntegrityError:
                None
        logging.info('USERS created.')
        logging.info('Creating PERSONS.')
        for person in PERSON_DATA:
            try:
                created_person = self.create_person(*person)
                created_person_preferences = PersonPreferences.objects.create(person=created_person)
                created_person_preferences.preferred_poses.add(random.choice(PosesList.objects.all()))
                created_person_preferences.preferred_poses.add(random.choice(PosesList.objects.all()))
                created_person_preferences.preferred_poses.add(random.choice(PosesList.objects.all()))
                created_person_preferences.preferred_poses.add(random.choice(PosesList.objects.all()))
                created_person_preferences.preferred_places.add(random.choice(PlacesList.objects.all()))
                created_person_preferences.preferred_places.add(random.choice(PlacesList.objects.all()))
                created_person_preferences.preferred_places.add(random.choice(PlacesList.objects.all()))
                created_person_preferences.preferred_places.add(random.choice(PlacesList.objects.all()))
                created_personal_settings = PersonalSettings.objects.create(person=created_person)
                created_person_periodicalnotification = PeriodicalNotification.objects.create(
                    person=created_person,
                    message="Wellcome! Don't hesitate to make your first check in.")
                created_person_tipnotification = TipNotification.objects.create(
                    person=created_person,
                    message="Wellcome! Go to your profile settings if you don't want to get useful tips.")
                created_person_differencenotification = DifferenceNotification.objects.create(
                    person=created_person,
                    message="Wellcome! Once you're in a relation you'll start getting difference notifications.")
                created_person_preferences.save()
                created_personal_settings.save()
                created_person_periodicalnotification.save()
                created_person_tipnotification.save()
                created_person_differencenotification.save()
                created_person.save()
            except IntegrityError:
                None
        logging.info('PERSONS created.')

    def create_user(self, username, password, first_name, last_name):
        return User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name,)

    def create_person(self, username, gender, birth_date, city):
        return Person.objects.create(user=User.objects.get(username=username), gender=gender, birth_date=birth_date, city=city,)
