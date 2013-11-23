from django.db import models
from django.core.exceptions import ValidationError
from fuck_book import settings


def get_upload_file_name(instance, filename):
    return 'profile_photos/{}_{}{}'.format(instance.user.username, instance.user.id, str(filename[filename.rfind('.'):len(filename)]))


class Person(models.Model):
    user = models.OneToOneField('auth.User')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    city = models.CharField('City', max_length=255, blank=True, null=True)
    photo = models.FileField(upload_to=get_upload_file_name, verbose_name="Profile photo", blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class PersonPreferences(models.Model):
    person = models.OneToOneField('persons.Person')
    relation = models.OneToOneField('persons.Person',
                                    related_name='related user',
                                    blank=True,
                                    null=True,
                                    error_messages={'unique': 'This person is already in a relation with another user!'})
    preferred_poses = models.ManyToManyField('hardcoded_models.PosesList', blank=True, null=True)
    preferred_places = models.ManyToManyField('hardcoded_models.PlacesList', blank=True, null=True)

    def __str__(self):
        return self.person.__str__()

    def save(self, *args, **kwargs):
        '''Redefined save method to handle creation of the relation between 2 Persons.
        It sets the relation for both Persons.
        Works in the oposite direction, removes relation for both persons

        '''
        super(PersonPreferences, self).save(*args, **kwargs)

        if self.relation and self.relation.personpreferences.relation != self.person:
            self.relation.personpreferences.relation = self.person
            self.relation.personpreferences.save()

        if not self.relation and Person.objects.filter(personpreferences__relation=self.person).exists():
            other_person = Person.objects.get(personpreferences__relation=self.person)
            other_person.personpreferences.relation = None
            other_person.personpreferences.save()

    def clean(self):
        '''Redefined clean method to make sure relation cannot be set to self.

        '''
        super(PersonPreferences, self).clean()
        if self.person == self.relation:
            raise ValidationError('One person cannot be related to itself')


class PersonalSettings(models.Model):
    person = models.OneToOneField('persons.Person')
    display_periodical_notification = models.BooleanField(default=True)
    display_tip_notification = models.BooleanField(default=True)
    display_difference_notification = models.BooleanField(default=True)

    periodical_notification_period = models.IntegerField(default=14)
    tip_notification_period = models.IntegerField(default=7)
    difference_notification_period = models.IntegerField(default=30)

    def __str__(self):
        return self.person.__str__()
