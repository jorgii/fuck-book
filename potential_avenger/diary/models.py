from django.db import models


from users.models import Person


class Diary(models.Model):
    person1 = models.ForeignKey(Person)
    person2 = models.ForeignKey(Person, related_name='diary related user', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
