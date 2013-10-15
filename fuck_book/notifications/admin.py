from django.contrib import admin

from .models import PeriodicalNotification, TipNotification, DifferenceNotification


admin.site.register(PeriodicalNotification)
admin.site.register(TipNotification)
admin.site.register(DifferenceNotification)
