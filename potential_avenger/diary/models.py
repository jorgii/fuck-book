from django.db import models
from django.contrib.auth.models import User


class Diary(models.Model):
    user1 = models.OneToOneField(User)
    user2 = models.OneToOneField(User, related_name='related user')
    timestamp = models.DateTimeField(auto_now_add=True)
