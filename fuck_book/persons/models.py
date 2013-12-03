from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


def get_upload_file_name(instance, filename):
    return 'profile_photos/{}_{}{}'.format(instance.user.username, instance.user.id, str(filename[filename.rfind('.'):len(filename)]))


class Person(models.Model):
    user = models.OneToOneField('auth.User')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    ORIENTATION_CHOICES = (
        ('H', 'Heterosexual'),
        ('L', 'Lesbian'),
        ('G', 'Gay'),
        ('BM', 'Bisexual(Male)'),
        ('BF', 'Bisexual(Female)'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    city = models.CharField('City', max_length=255, blank=True, null=True)
    nickname = models.CharField('Nickname', max_length=255, blank=True, null=True)
    orientation = models.CharField(max_length=1, choices=ORIENTATION_CHOICES, blank=True, null=True)
    photo = ProcessedImageField(upload_to=get_upload_file_name,
                                       verbose_name="Profile photo",
                                       processors=[ResizeToFit(500,500,upscale=False)],
                                       format='JPEG',
                                       options={'quality':60})
    preferred_poses = models.ManyToManyField('hardcoded_models.PosesList', blank=True, null=True)
    preferred_places = models.ManyToManyField('hardcoded_models.PlacesList', blank=True, null=True)
    display_periodical_notification = models.BooleanField(default=True)
    display_tip_notification = models.BooleanField(default=True)
    display_difference_notification = models.BooleanField(default=True)

    periodical_notification_period = models.IntegerField(default=14)
    tip_notification_period = models.IntegerField(default=7)
    difference_notification_period = models.IntegerField(default=30)
