from datetime import date, datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models.loading import cache as model_cache
if not model_cache.loaded:
    model_cache.get_models()

from checkin.models import CheckinDetails
from checkin.forms import CheckinForm
from notifications.models import PeriodicalNotification


class CheckinTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person
        self.person2 = User.objects.get(username='user2').person
        self.person3 = User.objects.get(username='user3').person
        self.person4 = User.objects.get(username='user4').person
        self.single_checkin = CheckinDetails.objects.create(creator=self.person1, datetime_created=datetime.now(), address='Sofia', rating=1)

    def test_create_checkin(self):
        self.assertTrue(isinstance(self.single_checkin, CheckinDetails))
        self.assertEqual(str(self.single_checkin), str(self.single_checkin.datetime_created) + ', ' + str(self.single_checkin.creator.user))

    def test_checkin_with_negative_duration(self):
        self.single_checkin.duration = -1
        self.single_checkin.save()
        self.assertRaises(ValidationError, self.single_checkin.clean)

    def test_checkin_with_duration_over_600(self):
        self.single_checkin.duration = 601
        self.single_checkin.save()
        self.assertRaises(ValidationError, self.single_checkin.clean)

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

class CheckinFormTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person
        self.person2 = User.objects.get(username='user2').person
        self.person3 = User.objects.get(username='user3').person
        self.person4 = User.objects.get(username='user4').person
        self.checkin_data = {'address':'Sofia',
                              'duration':30,
                              'rating':3,
                             }
        self.checkin_form = CheckinForm(self.checkin_data)
        self.checkin_form.instance = CheckinDetails(creator=self.person1)

    def test_single_checkin(self):
        if self.checkin_form.is_valid():
            self.instance = self.checkin_form.save()
            self.assertEqual(self.instance.creator, self.person1)
            self.assertContains(self.instance.participants, self.person1)
        else:
            raise ValidationError(self.checkin_form.errors)

    def test_multiple_checkin(self):
        self.checkin_form.data['participants'] = ['2', '3']
        if self.checkin_form.is_valid():
            self.instance = self.checkin_form.save()
            self.assertEqual(self.instance.participants, [self.person1, self.person2, self.person3])
        else:
            raise ValidationError(self.checkin_form.errors)