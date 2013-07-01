from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from notifications.models import PeriodicalNotification, TipNotification, DifferenceNotification
from users.models import PersonalSettings


@login_required
def notifications(request):
    current_person = request.user.person
    current_person_settings = PersonalSettings.objects.get(person=current_person)
    periodical_notifications = PeriodicalNotification.objects.filter(person=current_person).order_by('-date_saved')
    tip_notifications = TipNotification.objects.filter(person=current_person).order_by('-date_saved')
    difference_notifications = DifferenceNotification.objects.filter(person=current_person).order_by('-date_saved')
    if request.method == 'POST':
        notification_key = int(request.POST.get('notification_id'))
        notification_cls = request.POST.get('notification_class')
        mark_notification_as_read(notification_key, notification_cls)
    csrf(request)
    return render(request, "notifications.html", locals())


def mark_notification_as_read(key, cls):
    if cls == "PeriodicalNotification":
        notification = PeriodicalNotification.objects.get(id=key)
    elif cls == "TipNotification":
        notification = TipNotification.objects.get(id=key)
    else:
        notification = DifferenceNotification.objects.get(id=key)
    notification.unread = False
    notification.save(update_fields=['unread'])
