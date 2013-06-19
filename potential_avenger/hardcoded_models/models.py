from django.db import models


class PosesList(models.Model):
    pose = models.CharField('Pose', max_length=255)

    def __str__(self):
        return self.pose


class PlacesList(models.Model):
    place = models.CharField('Place', max_length=255)

    def __str__(self):
        return self.place


class TipsList(models.Model):
    useful_tip = models.CharField('Useful Tip', max_length=255)

    def __str__(self):
        return self.useful_tip


class NotificationType(models.Model):
    notification_type = models.CharField('Notification Type', max_length=255)

    def __str__(self):
        return self.notification_type
