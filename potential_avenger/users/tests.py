from datetime import date
from time import time


from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


from users.models import Person, PersonPreferences, PersonalSettings, get_upload_file_name
from users.views import profile


class PersonTest(TestCase):
    def setUp(self):
        self.person1 = self.create_person(user=self.create_user())
        self.person1_preferences = self.create_person_preferences(person=self.person1)
        self.person1_personal_settings = self.create_personal_settings(person=self.person1)

        self.person2 = self.create_person(
            user=self.create_user(
                username='user2',
                password='pass2',
                first_name='user2 name1',
                last_name='user2 name2'),
            gender='F',
            birth_date=date(year=1990, day=12, month=12),
            city='Varna')
        self.person2_preferences = self.create_person_preferences(person=self.person2)
        self.person2_personal_settings = self.create_personal_settings(person=self.person2)

    def create_user(
            self,
            username='user1',
            password='pass1',
            first_name='user1 name1',
            last_name='user1 name1',):
        return User.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name)

    def create_person(
            self,
            user,
            gender='M',
            birth_date=date.today(),
            city='Sofia'):
        return Person.objects.create(
            user=user,
            gender=gender,
            birth_date=birth_date,
            city=city,)

    def create_person_preferences(
            self,
            person,
            relation=None):
        return PersonPreferences.objects.create(
            person=person,
            relation=relation)

    def create_personal_settings(
            self,
            person,
            useful_tips=False,
            notification_period=0):
        return PersonalSettings(
            person=person,
            useful_tips=useful_tips,
            notification_period=notification_period)

    def test_create_person(self):
        self.assertTrue(isinstance(self.person1, Person))
        self.assertEqual(str(self.person1), self.person1.user.first_name + ' ' + self.person1.user.last_name)

    def test_jpg_get_upload_file_name(self):
        filename = 'profilephoto.jpg'
        path = 'profile_photos/{}_{}{}'.format(str(time()).replace('.', '_'), self.person1.user.id, str(filename[filename.rfind('.'):len(filename)]))
        created_path = get_upload_file_name(self.person1, filename)
        self.assertEqual(path, created_path)

    def test_person_relation_save(self):
        self.person1_preferences.relation = self.person2
        self.person1_preferences.save()
        self.assertEqual(self.person1_preferences.relation, self.person2)
        self.assertEqual(self.person2_preferences.relation, self.person1)
