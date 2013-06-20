from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


from users.models import Person, PersonPreferences, PersonalSettings


class UserForm(ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['gender', 'birth_date', 'city', 'photo']


class PersonPreferencesForm(ModelForm):
    class Meta:
        model = PersonPreferences
        fields = ['relation', 'preferred_poses', 'preferred_places']


class PersonalSettingsForm(ModelForm):
    class Meta:
        model = PersonalSettings
        fields = ['useful_tips', 'notification_period']
