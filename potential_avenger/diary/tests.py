from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


from diary.models import Diary
from diary.views import get_checkins_for_diary
from checkin.models import CheckinDetails


class DiaryTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json', 'diary_data.json', 'checkin_data.json', 'hardcoded_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person
        self.person2 = User.objects.get(username='user2').person

    def test_get_checkins_for_diary(self):
        diary = Diary.objects.get(person1=self.person1, person2=self.person2)
        expected_checkins = list(CheckinDetails.objects.filter(person=self.person1,
                                                               with_who=self.person2))
        expected_checkins.extend(CheckinDetails.objects.filter(person=self.person2,
                                                               with_who=self.person1))
        expected_checkins = sorted(expected_checkins, key=lambda x: x.date_checked, reverse=True)
        self.assertEqual(expected_checkins, get_checkins_for_diary(diary))

    def test_diary_get(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.get('/diary/')
        self.assertEqual(response.status_code, 200)
