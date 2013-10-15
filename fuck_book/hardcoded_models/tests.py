from django.test import TestCase
from django.test.client import Client

from hardcoded_models.models import PosesList, PlacesList, TipsList


class HardcodedModelsTest(TestCase):
    fixtures = ['hardcoded_data.json']

    def setUp(self):
        self.client = Client()
        self.pose = PosesList.objects.get(id=1)
        self.place = PlacesList.objects.get(id=1)
        self.tip = TipsList.objects.get(id=1)

    def test_create_pose(self):
        self.assertTrue(isinstance(self.pose, PosesList))
        self.assertEqual(str(self.pose), str(self.pose.pose))

    def test_create_place(self):
        self.assertTrue(isinstance(self.place, PlacesList))
        self.assertEqual(str(self.place), str(self.place.place))

    def test_create_tip(self):
        self.assertTrue(isinstance(self.tip, TipsList))
        self.assertEqual(str(self.tip), str(self.tip.useful_tip))
