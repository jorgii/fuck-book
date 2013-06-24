from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notifications.models import PeriodicalNotification, TipNotification, DifferenceNotification


@login_required
def notifications(request):
    current_user_id = request.user.id
    # To do: add if-else statement that checks if the user wants each kind of notifications
    periodical_notifications = PeriodicalNotification.objects.filter(person=current_user_id).order_by('-date_saved')
    tip_notifications = TipNotification.objects.filter(person=current_user_id).order_by('-date_saved')
    difference_notifications = DifferenceNotification.objects.filter(person=current_user_id).order_by('-date_saved')
    return render(request, "notifications.html", locals())
