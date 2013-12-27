from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


from diary.models import Diary
from checkin.models import CheckinDetails

class DiaryTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json']

    def setUp(self):
        self.client = Client()
        
        self.person1 = User.objects.get(username='user1').person
        self.person2 = User.objects.get(username='user2').person
        self.person3 = User.objects.get(username='user3').person
        self.person4 = User.objects.get(username='user4').person
        
        self.checkin1 = CheckinDetails.objects.create(creator=self.person1, rating=3, duration=30)
        self.checkin1.participants.add(self.person1, self.person2, self.person3)
        
        self.checkin2 = CheckinDetails.objects.create(creator=self.person2, rating=3, duration=30)
        self.checkin2.participants.add(self.person1, self.person2, self.person3)
        
        self.checkin3 = CheckinDetails.objects.create(creator=self.person3, rating=3, duration=30)
        self.checkin3.participants.add(self.person1, self.person2, self.person3)
        
        self.checkin4 = CheckinDetails.objects.create(creator=self.person4, rating=3, duration=30)
        self.checkin4.participants.add(self.person1, self.person2, self.person4)
        
        self.checkin5 = CheckinDetails.objects.create(creator=self.person1, rating=3, duration=30)
        self.checkin5.participants.add(self.person1, self.person2, self.person4)
        
        self.empty_checkin = CheckinDetails.objects.create(creator=self.person1, rating=3, duration=30)
        self.empty_checkin.participants.add(self.person1)
        
        self.diary1 = Diary.objects.create(creator=self.person1)
        self.diary1.checkins.add(self.checkin1, self.checkin2, self.checkin3)
        self.diary1.participants.add(self.person1, self.person2, self.person3)
        
        self.diary2 = Diary.objects.create(creator=self.person4)
        self.diary2.checkins.add(self.checkin4, self.checkin5)
        self.diary2.participants.add(self.person1, self.person2, self.person4)
        
        self.empty_diary = Diary.objects.create(creator=self.person1)
        self.empty_diary.participants.add(self.person1)

    def test_diary_str(self):
        self.assertEqual(str(self.diary1), 'DateTime: {},Creator: {},Participants: {}'.format(self.diary1.datetime_created, str(self.diary1.creator.user.username), [str(p.user.username) for p in self.diary1.participants.all()]))


    def test_diary_get(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.get('/diary/')
        self.assertEqual(response.status_code, 200)

    def test_empty_diary(self):
        self.client.login(username='user7', password='pass7')
        response = self.client.get('/diary/')
        received_diary_list = response.context['diary_list']
        self.assertEqual(list(), received_diary_list)

    def test_get_diaries_for_people(self):
        expected_diary_list = [self.diary1, self.diary2, self.empty_diary]
        received_diary_list = Diary.get_diaries_for_people(self.person1)
        self.assertItemsEqual(expected_diary_list, received_diary_list)

        expected_diary_list = [self.diary1, self.diary2]
        received_diary_list = Diary.get_diaries_for_people(self.person1, self.person2)
        self.assertItemsEqual(expected_diary_list, received_diary_list)

    def test_get_diary_for_exact_people(self):
        self.assertEqual(self.diary1, Diary.get_diary_for_exact_people(self.person1, self.person2, self.person3))
        self.assertEqual(self.diary2, Diary.get_diary_for_exact_people(self.person1, self.person2, self.person4))
        self.assertEqual(self.empty_diary, Diary.get_diary_for_exact_people(self.person1))

    def test_create(self):
        checkin = CheckinDetails.objects.create(creator=self.person4, rating=3, duration=30)
        created_diary = Diary.create(creator=self.person4, participants=[self.person1, self.person2, self.person4], checkins=checkin)
        self.assertIsInstance(created_diary, Diary)
        self.assertEqual(created_diary.creator, self.person4)
        self.assertItemsEqual(created_diary.participants.all(), [self.person1, self.person2, self.person4])
        self.assertItemsEqual(created_diary.checkins.all(), [checkin])
