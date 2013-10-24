from datetime import date

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from users.models import PersonalSettings, PersonPreferences
from notifications.models import PeriodicalNotification, TipNotification, DifferenceNotification, create_tip_message
from notifications.views import mark_notification_as_read
from checkin.models import CheckinDetails
from hardcoded_models.models import PosesList, PlacesList
from notifications.management.commands.send_difference_notification import Command


class NotificationTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json', 'notifications_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person
        self.periodical_notification = PeriodicalNotification.objects.get(id=1)
        self.tip_notification = TipNotification.objects.get(id=1)
        self.difference_notification = DifferenceNotification.objects.get(id=1)

    def test_create_periodical_notification(self):
        self.assertTrue(isinstance(self.periodical_notification, PeriodicalNotification))
        self.assertEqual(str(self.periodical_notification), str(self.periodical_notification.date_saved) + ', ' + str(self.periodical_notification.person.user))

    def test_create_tip_notification(self):
        self.assertTrue(isinstance(self.tip_notification, TipNotification))
        self.assertEqual(str(self.tip_notification), str(self.tip_notification.date_saved) + ', ' + str(self.tip_notification.person.user))

    def test_create_difference_notification(self):
        self.assertTrue(isinstance(self.difference_notification, DifferenceNotification))
        self.assertEqual(str(self.difference_notification), str(self.difference_notification.date_saved) + ', ' + str(self.difference_notification.person.user))

    def test_create_tip_message(self):
        tip_notification2 = TipNotification.objects.create(person=self.person1,
                                                           message=create_tip_message,
                                                           date_saved=date.today(),
                                                           unread=True)
        self.assertEqual("Sorry, no tips in the database.", str(tip_notification2.message()))

    def test_notifications_get(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('notifications')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_notifications_get_post(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('notifications')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = dict(notification_id='1',
                    notification_class='PeriodicalNotification')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_mark_notification_as_read_for_tip_notifications(self):
        mark_notification_as_read(key=2, cls="TipNotification")
        self.assertFalse(TipNotification.objects.get(id=2).unread)

    def test_mark_notification_as_read_for_difference_notifications(self):
        mark_notification_as_read(key=2, cls="DifferenceNotification")
        self.assertFalse(DifferenceNotification.objects.get(id=2).unread)


class CommandsTestCase(TestCase):
    fixtures = ['users_data.json', 'persons_data.json', 'notifications_data.json', 'hardcoded_data.json']

    def setUp(self):
        self.person1 = User.objects.get(username='user1').person
        self.person2 = User.objects.get(username='user2').person
        self.person1_settings = PersonalSettings.objects.get(person=self.person1)
        self.person1_preferences = PersonPreferences.objects.get(person=self.person1)
        self.pose = PosesList.objects.get(id=1)
        self.place = PlacesList.objects.get(id=1)
        self.cmd = Command()

    def test_send_periodical_notification(self):
        self.person1_settings.periodical_notification_period = 1
        self.person1_settings.save(update_fields=['periodical_notification_period'])
        args = []
        opts = {}
        call_command('send_periodical_notification', *args, **opts)
        self.assertTrue(PeriodicalNotification.objects.get(person=self.person1, date_saved=date.today()))

    def test_send_tip_notification(self):
        self.person1_settings.tip_notification_period = 1
        self.person1_settings.save(update_fields=['tip_notification_period'])
        args = []
        opts = {}
        call_command('send_tip_notification', *args, **opts)
        self.assertTrue(TipNotification.objects.get(person=self.person1, date_saved=date.today()))

    def test_send_difference_notification(self):
        self.person1_settings.difference_notification_period = 1
        self.person1_settings.save(update_fields=['difference_notification_period'])
        self.person1_preferences.relation = self.person2
        self.person1_preferences.save(update_fields=['relation'])
        args = []
        opts = {}
        call_command('send_difference_notification', *args, **opts)
        self.assertTrue(DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()))
        self.assertEqual("Not enough data yet. You have to check in more often. ;)", DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()).message)

    def test_send_difference_notification_with_checkin(self):
        self.person1_settings.difference_notification_period = 1
        self.person1_settings.save(update_fields=['difference_notification_period'])
        self.person1_preferences.relation = self.person2
        self.person1_preferences.save(update_fields=['relation'])
        CheckinDetails.objects.create(person=self.person1,
                                      date_checked=date(year=2013, month=7, day=3),
                                      address="Sofia, Bulgaria",
                                      rating=3,
                                      duration=30,
                                      with_who=self.person2,)
        args = []
        opts = {}
        call_command('send_difference_notification', *args, **opts)
        self.assertTrue(DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()))
        self.assertEqual("If you want to get these, you have to specify poses and places when you checkin.", DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()).message)

    def test_send_difference_notification_with_checkin_with_poses_and_places(self):
        self.person1_settings.difference_notification_period = 1
        self.person1_settings.save(update_fields=['difference_notification_period'])
        self.person1_preferences.relation = self.person2
        self.person1_preferences.save(update_fields=['relation'])
        checkin = CheckinDetails.objects.create(person=self.person1,
                                                date_checked=date(year=2013, month=7, day=3),
                                                address="Sofia, Bulgaria",
                                                rating=3,
                                                duration=30,
                                                with_who=self.person2,)
        checkin.poses.add(self.pose)
        checkin.places.add(self.place)
        checkin.save()
        args = []
        opts = {}
        call_command('send_difference_notification', *args, **opts)
        self.assertTrue(DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()))
        self.assertEqual("Damn, you're selfish! You need to think more about what poses and places your partner likes.", DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()).message)

    def test_send_difference_notification_with_checkin_with_no_preferred_poses_and_places(self):
        self.person1_settings.difference_notification_period = 1
        self.person1_settings.save(update_fields=['difference_notification_period'])
        self.person1_preferences.relation = self.person2
        self.person1_preferences.save(update_fields=['relation'])
        checkin = CheckinDetails.objects.create(person=self.person1,
                                                date_checked=date(year=2013, month=7, day=3),
                                                address="Sofia, Bulgaria",
                                                rating=3,
                                                duration=30,
                                                with_who=self.person2,)
        checkin.poses.add(self.pose)
        checkin.places.add(self.place)
        checkin.save()
        self.person2.personpreferences.preferred_poses.clear()
        args = []
        opts = {}
        call_command('send_difference_notification', *args, **opts)
        self.assertTrue(DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()))
        self.assertEqual("Your partner hasn't specified all of his/her preferences yet.", DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()).message)

    def test_count_matching_items(self):
        preferred_poses = PosesList.objects.all()
        poses_counter = self.cmd.get_items_usage(preferred_poses)
        matching_poses = self.cmd.count_matching_items(preferred_items=preferred_poses, items_counter=poses_counter, half=2)
        self.assertEqual(2, matching_poses)

    def test_send_difference_notification_with_checkin_with_preferred_poses_and_places(self):
        self.person1_settings.difference_notification_period = 1
        self.person1_settings.save(update_fields=['difference_notification_period'])
        self.person1_preferences.relation = self.person2
        self.person1_preferences.save(update_fields=['relation'])
        checkin = CheckinDetails.objects.create(person=self.person1,
                                                date_checked=date(year=2013, month=7, day=3),
                                                address="Sofia, Bulgaria",
                                                rating=3,
                                                duration=30,
                                                with_who=self.person2,)
        checkin.poses = self.person2.personpreferences.preferred_poses.get_query_set()
        checkin.places.add(self.place)
        checkin.save()
        args = []
        opts = {}
        call_command('send_difference_notification', *args, **opts)
        self.assertTrue(DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()))
        self.assertEqual("You're doing good with the poses, but try to spice it up with some places your partner likes.", DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()).message)

    def test_send_difference_notification_with_checkin_with_poses_and_preferred_places(self):
        self.person1_settings.difference_notification_period = 1
        self.person1_settings.save(update_fields=['difference_notification_period'])
        self.person1_preferences.relation = self.person2
        self.person1_preferences.save(update_fields=['relation'])
        checkin = CheckinDetails.objects.create(person=self.person1,
                                                date_checked=date(year=2013, month=7, day=3),
                                                address="Sofia, Bulgaria",
                                                rating=3,
                                                duration=30,
                                                with_who=self.person2,)
        checkin.poses.add(self.pose)
        checkin.places = self.person2.personpreferences.preferred_places.get_query_set()
        checkin.save()
        args = []
        opts = {}
        call_command('send_difference_notification', *args, **opts)
        self.assertTrue(DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()))
        self.assertEqual("You're doing good with the places, but you need to think more about what poses your partner likes.", DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()).message)

    def test_send_difference_notification_with_checkin_with_preferred_poses_and_preferred_places(self):
        self.person1_settings.difference_notification_period = 1
        self.person1_settings.save(update_fields=['difference_notification_period'])
        self.person1_preferences.relation = self.person2
        self.person1_preferences.save(update_fields=['relation'])
        checkin = CheckinDetails.objects.create(person=self.person1,
                                                date_checked=date(year=2013, month=7, day=3),
                                                address="Sofia, Bulgaria",
                                                rating=3,
                                                duration=30,
                                                with_who=self.person2,)
        checkin.poses = self.person2.personpreferences.preferred_poses.get_query_set()
        checkin.places = self.person2.personpreferences.preferred_places.get_query_set()
        checkin.save()
        args = []
        opts = {}
        call_command('send_difference_notification', *args, **opts)
        self.assertTrue(DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()))
        self.assertEqual("Nice to see you care about what your partner likes. Keep up the good 'work'! ;)", DifferenceNotification.objects.get(person=self.person1, date_saved=date.today()).message)

    def test_calculate_half_of_used_items(self):
        preferred_poses = ['leg_lock', 'missionary', 'advanced_sex', 'water_sex']
        poses_counter = self.cmd.get_items_usage(preferred_poses)
        half = self.cmd.calculate_half_of_used_items(poses_counter)
        self.assertEqual(2, half)
