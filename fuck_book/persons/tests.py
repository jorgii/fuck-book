from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models import Q


from notifications.models import PeriodicalNotification, TipNotification, DifferenceNotification
from persons.models import Person, get_upload_file_name
from persons.views import get_number_of_unread_notifications


class PersonTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person
        self.person2 = User.objects.get(username='user2').person

    def person_post_data(self, user):
        return dict(first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    gender=user.person.gender,
                    birth_date=user.person.birth_date,
                    city=user.person.city,
                    periodical_notification_period=user.person.periodical_notification_period,
                    tip_notification_period=user.person.tip_notification_period,
                    difference_notification_period=user.person.difference_notification_period,)

    def test_create_person(self):
        self.assertEqual(str(self.person1), self.person1.user.first_name + ' ' + self.person1.user.last_name)

    def test_jpg_get_upload_file_name(self):
        filename = 'profilephoto.jpg'
        path = 'profile_photos/{}_{}{}'.format(self.person1.user.username, self.person1.user.id, str(filename[filename.rfind('.'):len(filename)]))
        created_path = get_upload_file_name(self.person1, filename)
        self.assertEqual(path, created_path)

    def test_get_unread_notifications(self):
        PeriodicalNotification.objects.create(person=self.person1,
                                              message="Wellcome! Don't hesitate to make your first check in.")
        TipNotification.objects.create(person=self.person1,
                                       message="Wellcome! Go to your profile settings if you don't want to get useful tips.")
        DifferenceNotification.objects.create(person=self.person1,
                                              message="Wellcome! Once you're in a relation you'll start getting difference notifications.")
        self.assertEqual(3, get_number_of_unread_notifications(self.person1))

    def test_person_relation_save(self):
        self.person1.relation = self.person2
        self.person1.save()
        self.assertEqual(self.person1.relation, self.person2)
        self.assertEqual(self.person2.relation, self.person1)

    def test_related_to_self(self):
        self.person1.relation = self.person1
        self.person1.save()
        self.assertRaises(ValidationError, self.person1.clean)

    def test_view_login_get_post(self):
        url = reverse('login',)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, dict(username='user1', password='pass1'))
        self.assertEqual(response.status_code, 302)

    def test_view_profile_get(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('profile', args=[self.person1.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_other_profile_get(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('profile', args=[self.person2.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_profile_empty_birthday(self):
        self.client.login(username='user1', password='pass1')
        self.person1.birth_date = None
        self.person1.save()
        url = reverse('profile', args=[self.person1.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_profile_no_mandatory_data(self):
        self.person1.birth_date = None
        self.person1.city = None
        self.client.login(username='user1', password='pass1')
        url = reverse('profile', args=[self.person1.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_profile_edit_get_post(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('profile_edit')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = response.context['user']
        data = self.person_post_data(user)
        data['email'] = 'asd@asd.asd'
        data['first_name'] = 'changed firstname'
        data['periodical_notification_period'] = 66
        response = self.client.post(url, data)
        expected_url = reverse('profile', args=[self.person1.user.username])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        self.assertEqual(User.objects.get(username='user1').email, data['email'])
        self.assertEqual(User.objects.get(username='user1').first_name, data['first_name'])
        self.assertEqual(User.objects.get(username='user1').person.periodical_notification_period, data['periodical_notification_period'])

    def test_home_get(self):
        url = reverse('home')
        self.client.login(username='user1', password='pass1')
        response = self.client.get(url)
        expected_url = reverse('profile', args=[self.person1.user.username])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_register_get(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_register_post(self):
        url = reverse('register')
        response = self.client.post(url, dict(username='newone', password1='newpass', password2='newpass'))
        expected_url = reverse('register_success')
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_register_success_get_post(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('register_success')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = response.context.__getitem__('user')
        data = self.person_post_data(user)
        data['email'] = 'asd@asd.asd'
        data['first_name'] = 'changed firstname'
        del data['periodical_notification_period']
        del data['tip_notification_period']
        del data['difference_notification_period']
        response = self.client.post(url, data)
        expected_url = reverse('profile', args=[self.person1.user.username])
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        self.assertEqual(User.objects.get(username='user1').email, data['email'])
        self.assertEqual(User.objects.get(username='user1').first_name, data['first_name'])


class FormsTest(TestCase):
    fixtures = ['users_data.json', 'persons_data.json', 'hardcoded_data.json']

    def setUp(self):
        self.client = Client()
        self.person1 = User.objects.get(username='user1').person
        self.person2 = User.objects.get(username='user2').person

    def test_personpreferences_init_with_relation(self):
        self.client.login(username='user1', password='pass1')
        self.person1.relation = self.person2
        self.person1.save()
        url = reverse('profile_edit')
        response = self.client.get(url)
        received_relation_queryset = response.context['person_form'].fields['relation'].queryset
        expected_relation_queryset = Person.objects.exclude(id=self.person1.id).filter(
            Q(relation=None) | Q(id=self.person1.relation.id)
        )
        self.assertQuerysetEqual(received_relation_queryset, map(repr, expected_relation_queryset), ordered=False)

    def test_personpreferences_init_with_no_relation(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('profile_edit')
        response = self.client.get(url)
        received_relation_queryset = response.context['person_form'].fields['relation'].queryset
        expected_relation_queryset = Person.objects.exclude(
            id=self.person1.id).filter(relation=None)
        self.assertQuerysetEqual(received_relation_queryset, map(repr, expected_relation_queryset), ordered=False)
