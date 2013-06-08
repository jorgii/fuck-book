from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^profile', 'users.views.profile', name='profile'),
    url(r'^checkin', 'checkin.views.checkin', name='checkin'),
    url(r'^diary', 'diary.views.diary', name='diary'),
    url(r'^statistics', 'statistics.views.statistics', name='statistics'),
    url(r'^notifications', 'notifications.views.notifications', name='notifications'),
    url(r'^dice', 'dice.views.dice', name='dice'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
