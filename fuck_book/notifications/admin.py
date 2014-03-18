from django.contrib import admin

from .models import NotificationTypes, NotificationInstance


admin.site.register(NotificationTypes)
admin.site.register(NotificationInstance)
