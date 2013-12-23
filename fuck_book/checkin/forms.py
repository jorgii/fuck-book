from django.forms import ModelForm

from checkin.models import CheckinDetails


class CheckinForm(ModelForm):

    class Meta:
        model = CheckinDetails
        fields = [
            'address',
            'poses',
            'places',
            'rating',
            'duration',
            'contraception',
            'participants']

    def save(self):
        instance = super(CheckinForm, self).save()
        if instance.creator not in instance.participants.all():
            instance.participants.add(instance.creator)
        return instance