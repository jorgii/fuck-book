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
