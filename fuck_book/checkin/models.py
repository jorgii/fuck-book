from datetime import date

from django.db import models
from django.core.exceptions import ValidationError


class CheckinDetails(models.Model):
    person = models.ForeignKey('users.Person')
    date_checked = models.DateField(default=date.today())
    address = models.CharField('Address (ex: Cherni vrah 47, Sofia, Bulgaria):', max_length=255)
    poses = models.ManyToManyField('hardcoded_models.PosesList', blank=True, null=True)
    places = models.ManyToManyField('hardcoded_models.PlacesList', blank=True, null=True)
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
    with_who = models.ForeignKey('users.Person', related_name='checkin_related_user', blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.date_checked, self.person.user)

    def clean(self):
        ''' Redefined clean method to make sure:
        - person cannot checkin with self
        - person cannot checkin with negative duration number
        - person cannot checkin with too large duration number
        '''
        super(CheckinDetails, self).clean()
        if self.person == self.with_who:
            raise ValidationError("'Loving' yourself might be great, but that's not what we're looking for here. ;)")
        if self.duration <= 0:
            raise ValidationError("Man! Either you were faster than the light's speed or you entered the wrong number. Try positive values the next time.")
        elif self.duration > 600:
            raise ValidationError("Always thought that 'all night long' was just an expression. Try a smaller number next time. :)")
