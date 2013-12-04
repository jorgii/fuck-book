from django.forms import ModelForm


from checkin.models import CheckinDetails


class CheckinForm(ModelForm):
    def __init__(self, data=None, instance=None, *args, **kwargs):
        super(CheckinForm, self).__init__(data=data, instance=instance, *args, **kwargs)
        with_who_set = self.fields['participants'].queryset
        self.fields['participants'].queryset = with_who_set.exclude(id=instance.person.id)

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
