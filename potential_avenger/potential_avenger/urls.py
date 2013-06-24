from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^profile_edit/$', 'users.views.profile_edit', name='profile_edit'),
    url(r'^profile/(?P<username>\w+)/$', 'users.views.profile', name='profile'),
    url(r'^checkin/$', 'checkin.views.checkin', name='checkin'),
    url(r'^diary/$', 'diary.views.diary', name='diary'),
    url(r'^statistics/$', 'statistics.views.statistics', name='statistics'),
    url(r'^notifications/$', 'notifications.views.notifications', name='notifications'),
    url(r'^dice/$', 'dice.views.dice', name='dice'),
    url(r'^$', 'users.views.home', name='home'),
    url(r'^login/$', 'users.views.login_user', name='login'),
    url(r'^register/$', 'users.views.register', name='register'),
    url(r'^register_success/$', 'users.views.register_success', name='register_success'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
