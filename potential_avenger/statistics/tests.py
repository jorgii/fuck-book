from datetime import date
from collections import OrderedDict


from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


from users.models import Person
from checkin.models import CheckinDetails
from statistics.views import get_checkins_grouped, average, get_top_three


class StatisticsTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = Person.objects.get(user=User.objects.get(username='user1'))

    def test_get_checkins_grouped_daily(self):
        expected_daily_checkins = OrderedDict()
        expected_daily_checkins[date(year=2013, month=3, day=3)] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2013, month=3, day=3))]
        expected_daily_checkins[date(year=2013, month=2, day=2)] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2013, month=2, day=2))]
        expected_daily_checkins[date(year=2013, month=1, day=1)] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2013, month=1, day=1))]
        expected_daily_checkins[date(year=2012, month=4, day=3)] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=4, day=3))]
        expected_daily_checkins[date(year=2012, month=3, day=2)] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=3, day=2))]
        expected_daily_checkins[date(year=2012, month=2, day=1)] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=2, day=1))]
        expected_daily_checkins[date(year=2012, month=1, day=3)] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=1, day=3))]
        expected_daily_checkins[date(year=2012, month=1, day=2)] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=1, day=2))]
        expected_daily_checkins[date(year=2012, month=1, day=1)] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=1, day=1))]
        result_daily_checkins = get_checkins_grouped(person=self.person1,
                                                     from_t=date(year=2012, month=1, day=1),
                                                     to_t=date(year=2013, month=3, day=3),
                                                     group_by='d')
        self.assertEqual(expected_daily_checkins, result_daily_checkins)

    def test_get_checkins_grouped_monthly(self):
        expected_monthly_checkins = OrderedDict()
        expected_monthly_checkins['3/2013'] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2013, month=3, day=3))]
        expected_monthly_checkins['2/2013'] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2013, month=2, day=2))]
        expected_monthly_checkins['1/2013'] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2013, month=1, day=1))]
        expected_monthly_checkins['4/2012'] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=4, day=3))]
        expected_monthly_checkins['3/2012'] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=3, day=2))]
        expected_monthly_checkins['2/2012'] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=2, day=1))]
        expected_monthly_checkins['1/2012'] = [CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=1, day=3)),
                                               CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=1, day=2)),
                                               CheckinDetails.objects.create(person=self.person1, address='Sofia', rating=1, date_checked=date(year=2012, month=1, day=1))]
        result_monthly_checkins = get_checkins_grouped(person=self.person1,
                                                       from_t=date(year=2012, month=1, day=1),
                                                       to_t=date(year=2013, month=3, day=3),
                                                       group_by='m')
        self.assertEqual(expected_monthly_checkins, result_monthly_checkins)

    def test_average_format(self):
        self.assertEqual('4.50', average(4, 5))
        self.assertEqual('5.00', average(4, 5, 6))

    def test_top_three(self):
        args = [1, 2, 3, 4, 2, 2, 6, 1, 1, 9, 9]
        top_three = get_top_three(*args)
        self.assertTrue(len(top_three) == 3)
        self.assertTrue(1 in top_three)
        self.assertTrue(2 in top_three)
        self.assertTrue(9 in top_three)

    def test_statistics_get(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.get('/statistics/')
        self.assertEqual(200, response.status_code)
