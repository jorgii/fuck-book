from datetime import date, datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from checkin.models import CheckinDetails
from notifications.models import PeriodicalNotification


class CheckinTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person
        self.checkin = CheckinDetails.objects.create(creator=self.person1, datetime_created=datetime.now(), address='Sofia', rating=1)

    def test_create_checkin(self):
        self.assertTrue(isinstance(self.checkin, CheckinDetails))
        self.assertEqual(str(self.checkin), str(self.checkin.datetime_created) + ', ' + str(self.checkin.creator.user))

    def test_checkin_with_negative_duration(self):
        self.checkin.duration = -1
        self.checkin.save()
        self.assertRaises(ValidationError, self.checkin.clean)

    def test_checkin_with_duration_over_600(self):
        self.checkin.duration = 601
        self.checkin.save()
        self.assertRaises(ValidationError, self.checkin.clean)

    def test_checkin_get(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('checkin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_checkin_get_post(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('checkin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        PeriodicalNotification.objects.create(person=self.person1,
                                              date_saved=date(year=2013, month=6, day=30),
                                              message="default message",
                                              unread=False)
        data = dict(creator=self.person1,
                    datetime_created=date.today(),
                    address='Sofia, Bulgaria',
                    rating=3,
                    duration=30,)
        response = self.client.post(url, data)
        expected_url = reverse('diary')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
