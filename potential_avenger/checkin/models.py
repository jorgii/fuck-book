from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    user = models.OneToOneField(User)
    latitude = models.DecimalField(max_digits=16, desimal_places=6)
    longitude = models.DecimalField(max_digits=16, desimal_places=6)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
