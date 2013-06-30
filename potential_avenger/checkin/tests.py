from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from checkin.models import CheckinDetails
from users.models import Person


class CheckinTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.person = self.create_person(user=self.create_user())
        # self.person_preferences = self.create_person_preferences(person=self.person)
        # self.person_personal_settings = self.create_personal_settings(person=self.person)
        # self.person_personal_settings.save()
        # self.person_preferences.save()
        self.person.save()
        self.checkin = slef.create_checkin(person=self.person)
        self.checkin.save()

    def create_user(self,
                    username='user1',
                    password='pass1',
                    first_name='user1 name1',
                    last_name='user1 name1',):
        return User.objects.create_user(username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,)

    def create_person(self,
                      user,
                      gender='M',
                      birth_date=date.today(),
                      city='Sofia'):
        return Person.objects.create(user=user,
                                     gender=gender,
                                     birth_date=birth_date,
                                     city=city,)

    def create_checkin(self,
                       person,
                       date_checked,
                       address='Cherni vrah 47, Sofia, Bulgaria',
                       poses=list('missionary', 'leg_lock', 'advanced_sex'),
                       places=list('doube_bed', 'desk'),
                       raiting='4',
                       duration,
                       contraception,
                       with_who=None):
        return CheckinDetails.objects.create(person=person,
                                             date_checked=date_checked,
                                             address=address,
                                             poses=poses,
                                             places=places,
                                             raiting=raiting,
                                             duration=duration,
                                             contraception=contraception,
                                             with_who=with_who,)
