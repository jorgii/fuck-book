from django.forms import ModelForm
from django.contrib.auth.models import User


from users.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['gender', 'birth_date', 'city']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
