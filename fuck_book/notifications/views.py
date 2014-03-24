from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf


from notifications.models import NotificationTypes, NotificationInstance


@login_required
def notifications(request):
    current_person = request.user.person

    notifications_by_type = dict()
    for notification_type in NotificationTypes.objects.all():
            notifications_by_type[notification_type.name]= NotificationInstance.objects.filter(person=current_person).filter(notification_type=notification_type).all()

    if request.method == 'POST':
        notification_key = int(request.POST.get('notification_id'))
        notification_cls = request.POST.get('notification_class')
        mark_notification_as_read(notification_key, notification_cls)
    csrf(request)
    return render(request, "notifications.html", locals())


def mark_notification_as_read(key, cls):
    ''' Takes:
    - key - an id of the notification the user wants to mark as read
    - cls - the class of this same notification
    Updates the notification's unread field from True to False so
    it won't be displayd as new any more.
    '''
#    if cls == "PeriodicalNotification":
#        notification = PeriodicalNotification.objects.get(id=key)
#    elif cls == "TipNotification":
#        notification = TipNotification.objects.get(id=key)
#    else:
#        notification = DifferenceNotification.objects.get(id=key)
#    notification.unread = False
#    notification.save(update_fields=['unread'])
