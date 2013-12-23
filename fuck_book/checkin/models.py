from django.db import models
from django.core.exceptions import ValidationError


class CheckinDetails(models.Model):
    creator = models.ForeignKey('persons.Person')
    datetime_created = models.DateTimeField(auto_now_add=True)
    longitude = models.DecimalField('Longitude', max_digits=9, decimal_places=6 ,null=True, blank=True)
    latitude = models.DecimalField('Latitude', max_digits=9, decimal_places=6, null=True, blank=True)
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
    participants = models.ManyToManyField('persons.Person', related_name='checkin_related_users', blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.datetime_created, self.creator.user)

    def clean(self):
        ''' Redefined clean method to make sure:
        - person cannot checkin with self
        - person cannot checkin with negative duration number
        - person cannot checkin with too large duration number
        '''
        super(CheckinDetails, self).clean()
        if self.duration <= 0:
            raise ValidationError("Man! Either you were faster than the light's speed or you entered the wrong number. Try positive values the next time.")
        elif self.duration > 600:
            raise ValidationError("Always thought that 'all night long' was just an expression. Try a smaller number next time. :)")

    @staticmethod
    def get_checkins_for_exact_people(*people):
        gathered_checkins = CheckinDetails.get_checkins_for_people(*people)
        for checkin in gathered_checkins:
            if checkin.participants.count() != len(people):
                gathered_checkins = gathered_checkins.exclude(id=checkin.id)
        return gathered_checkins

    @staticmethod
    def get_checkins_for_people(*people):
        for person in people:
            if person == people[0]:
                gathered_checkins = CheckinDetails.objects.filter(participants__id=person.id)
            else:
                gathered_checkins=gathered_checkins.filter(participants__id=person.id)
        return gathered_checkins
