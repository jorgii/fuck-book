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
    def __init__(self, data=None, instance=None, *args, **kwargs):
        super(PersonPreferencesForm, self).__init__(data=data, instance=instance, *args, **kwargs)
        relation_set = self.fields['relation'].queryset
        self.fields['relation'].queryset = relation_set.exclude(id=instance.person.id).filter(personpreferences__relation=None)

    class Meta:
        model = PersonPreferences
        fields = ['relation', 'preferred_poses', 'preferred_places']


class PersonalSettingsForm(ModelForm):
    class Meta:
        model = PersonalSettings
        exclude = ['person']
