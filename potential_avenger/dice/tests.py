from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from hardcoded_models.models import PosesList, PlacesList


class CheckinTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json', 'hardcoded_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person

    def test_dice_get(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('dice')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dice_get_with_empty_poses_list(self):
        PosesList.objects.all().delete()
        self.client.login(username='user1', password='pass1')
        url = reverse('dice')
        response = self.client.get(url)
        self.assertEqual("Sorry, no available poses to choose from.", response.context['random_pose'])
        self.assertEqual(response.status_code, 200)

    def test_dice_get_with_empty_places_list(self):
        PlacesList.objects.all().delete()
        self.client.login(username='user1', password='pass1')
        url = reverse('dice')
        response = self.client.get(url)
        self.assertEqual("Sorry, no available places to choose from.", response.context['random_place'])
        self.assertEqual(response.status_code, 200)
