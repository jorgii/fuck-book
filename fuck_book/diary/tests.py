from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


from diary.models import Diary


class DiaryTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person
        self.person2 = User.objects.get(username='user2').person

    def test_diary_str(self):
        diary = Diary.objects.get(person1=self.person1, person2=self.person2)
        self.assertEqual(str(diary), 'DateTime: {},Creator: {},Participants: {}'.format(diary.datetime_created, str(diary.creator.user.username), [str(p.user.username) for p in diary.participants.all()]))

    def test_diary_list_view(self):
        self.client.login(username='user1', password='pass1')
        expected_diary_list = list(Diary.objects.filter(person1=self.person1))
        expected_diary_list.extend(list(Diary.objects.filter(person2=self.person1)))
        expected_diary_list = sorted(expected_diary_list, key=lambda x: x.timestamp, reverse=True)
        response = self.client.get('/diary/')
        received_diary_list = response.context['diary_list']
        self.assertEqual(expected_diary_list, received_diary_list)

    def test_diary_get(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.get('/diary/')
        self.assertEqual(response.status_code, 200)

    def test_empty_diary(self):
        self.client.login(username='user7', password='pass7')
        response = self.client.get('/diary/')
        received_diary_list = response.context['diary_list']
        self.assertEqual(list(), received_diary_list)
