from django.db import models
from django.contrib.auth.models import User


class User1(models.Model):
    name = models.CharField('Name', max_length=255)
    user = models.OneToOneField(User)
