from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf


from notifications.models import NotificationInstance


@login_required
def notifications(request):
    current_person = request.user.person

    notifications_by_type = dict()
    for notification_type in current_person.notification_settings.keys():
        notifications_by_type[notification_type]= NotificationInstance.objects.filter(person=current_person).filter(notification_type__name=notification_type).all()

    if request.method == 'POST':
        notification_key = int(request.POST.get('notification_id'))
        mark_notification_as_read(notification_key)
    csrf(request)
    return render(request, "notifications.html", locals())


def mark_notification_as_read(key):
    ''' Takes:
    - key - an id of the notification the user wants to mark as read
    - cls - the class of this same notification
    Updates the notification's unread field from True to False so
    it won't be displayd as new any more.
    '''
    notification = NotificationInstance.objects.get(id=key)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
