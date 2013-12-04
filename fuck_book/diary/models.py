from django.db import models


class Diary(models.Model):
    creator = models.ForeignKey('persons.Person')
    participants = models.ManyToManyField('persons.Person', related_name='diary participants', blank=True, null=True)
    checkins = models.ManyToManyField('checkin.CheckinDetails')
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'DateTime: {},Creator: {},Participants: {}'.format(self.datetime_created, str(self.creator.user.username), [str(p.user.username) for p in self.participants.all()])
