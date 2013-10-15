from django.contrib import admin

from .models import Person, PersonPreferences, PersonalSettings


admin.site.register(Person)
admin.site.register(PersonPreferences)
admin.site.register(PersonalSettings)
