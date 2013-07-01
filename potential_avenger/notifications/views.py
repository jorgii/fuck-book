from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notifications.models import PeriodicalNotification, TipNotification, DifferenceNotification
from users.models import PersonalSettings


@login_required
def notifications(request):
    current_person = request.user.person
    current_person_settings = PersonalSettings.objects.get(person=current_person)
    periodical_notifications = PeriodicalNotification.objects.filter(person=current_person).order_by('-date_saved')
    tip_notifications = TipNotification.objects.filter(person=current_person).order_by('-date_saved')
    difference_notifications = DifferenceNotification.objects.filter(person=current_person).order_by('-date_saved')
    return render(request, "notifications.html", locals())
