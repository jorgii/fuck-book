from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from checkin.models import CheckinDetails
from users.models import Person


class CheckinTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json', 'checkin_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person
        self.person2 = User.objects.get(username='user2').person
        self.checkin = CheckinDetails.objects.get(id=1)

    def test_create_checkin(self):
        self.assertTrue(isinstance(self.checkin, CheckinDetails))
        self.assertEqual(str(self.checkin), str(self.checkin.date_checked) + ', ' + str(self.checkin.person.user))
