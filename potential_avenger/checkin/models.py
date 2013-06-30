from datetime import date

from django.db import models
from django.core.exceptions import ValidationError

from hardcoded_models.models import PosesList, PlacesList
from users.models import Person


class CheckinDetails(models.Model):
    person = models.ForeignKey(Person)
    date_checked = models.DateField(default=date.today())
    address = models.CharField('Address (ex: Cherni vrah 47, Sofia, Bulgaria):', max_length=255)
    poses = models.ManyToManyField(PosesList)
    places = models.ManyToManyField(PlacesList)
    RAITING_CHOICES = (
        ('1', '1 - Horrible'),
        ('2', '2 - Meh'),
        ('3', '3 - Average'),
        ('4', '4 - Quite good, actually'),
        ('5', '5 - Damn! That was awesome')
    )
    rating = models.CharField(max_length=1, choices=RAITING_CHOICES)
    duration = models.IntegerField('Duration (in minutes):', default=10)
    contraception = models.BooleanField('Contraception (y/n):', default=True)
    with_who = models.ForeignKey(Person,
                                 related_name='checkin related user',
                                 blank=True,
                                 null=True)

    def clean(self):
        super().clean()
        if self.person == self.with_who:
            raise ValidationError("'Loving' yourself might be great, but that's not what we're looking for here. ;)")
        if self.duration <= 0:
            raise ValidationError("Man! Either you were faster than the light's speed or you entered the wrong number. Try positive values the next time.")
        elif self.duration > 600:
            raise ValidationError("Always thought that 'all night long' was just an expression. Try a smaller number next time. :)")
