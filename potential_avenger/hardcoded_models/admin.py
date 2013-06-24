from django.contrib import admin

from .models import PosesList, PlacesList, TipsList


admin.site.register(PosesList)
admin.site.register(PlacesList)
admin.site.register(TipsList)
