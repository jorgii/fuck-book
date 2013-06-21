from datetime import date


from django.contrib.auth.models import User
from django.test import TestCase


from users.models import Person


class PersonTest(TestCase):

    def create_person(self):
        user = User.objects.create(username='person_test', password='pass')
        person = Person.objects.create(user=user, gender='M', birth_date=date.today())
        self.assertTrue(isinstance(person, Person))
