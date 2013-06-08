from django.db import models


class PosesList(models.Model):
    pose = models.CharField('Pose', max_length=255)


class PlacesList(models.Model):
    place = models.CharField('Place', max_length=255)


class TipsList(models.Model):
    useful_tip = models.CharField('Useful Tip', max_length=255)


class NotificationType(models.Model):
    notification_type = models.CharField('Notification Type', max_length=255)
