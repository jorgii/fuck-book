from datetime import date
from time import time


from django.contrib.auth.models import User
from django.test import TestCase


from users.models import Person, PersonPreferences, PersonalSettings, get_upload_file_name


class PersonTest(TestCase):

    def create_user(
            self,
            username='person_test',
            password='pass',
            first_name='fistname',
            last_name='lastname',):
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
        person = self.create_person(user=self.create_user())
        self.assertTrue(isinstance(person, Person))
        self.assertEqual(str(person), person.user.first_name + ' ' + person.user.last_name)

    def test_jpg_get_upload_file_name(self):
        person = self.create_person(user=self.create_user())
        filename = 'profilephoto.jpg'
        path = 'profile_photos/{}_{}{}'.format(str(time()).replace('.', '_'), person.user.id, str(filename[filename.rfind('.'):len(filename)]))
        created_path = get_upload_file_name(person, filename)
        self.assertEqual(path, created_path)

    def test_person_relation_save(self):
        person1 = self.create_person(user=self.create_user())
        person2 = self.create_person(
            user=self.create_user(
                username='user1',
                password='pass1',
                first_name='name1',
                last_name='name2'),
            gender='F',
            birth_date=date(year=1990, day=12, month=12),
            city='Varna')

        person_preferences1 = self.create_person_preferences(person=person1)
        person_preferences2 = self.create_person_preferences(person=person2)

        person_preferences1.relation = person2
        person_preferences1.save()
        print(person_preferences2.relation)
        self.assertEqual(person_preferences1.relation, person2)
        self.assertEqual(person_preferences2.relation, person1)
