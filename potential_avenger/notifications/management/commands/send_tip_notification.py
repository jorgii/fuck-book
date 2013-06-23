from django.core.management.base import BaseCommand, CommandError
from notifications.models import Notification


class Command(BaseCommand):
    