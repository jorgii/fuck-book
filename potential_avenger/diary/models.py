from django.db import models


class Diary(models.Model):
    person1 = models.ForeignKey('users.Person')
    person2 = models.ForeignKey('users.Person', related_name='diary related user', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.person2:
            return '{}, {}, {}'.format(self.timestamp, str(self.person1.user.username), str(self.person2.user.username))
        else:
            return '{}, {}, {}'.format(self.timestamp, str(self.person1.user.username), None)
