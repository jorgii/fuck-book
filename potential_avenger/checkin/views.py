from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from checkin.models import CheckinDetails
from checkin.forms import CheckinForm
from notifications.models import PeriodicalNotification
from users.models import PersonalSettings
from diary.models import Diary


@login_required
def checkin(request):
    this_person = request.user.person
    current_checkin = CheckinDetails(person=this_person)
    checkin_form = CheckinForm(request.POST or None, instance=current_checkin)

    if request.method == 'POST':
        if checkin_form.is_valid():
            checkin_form.save()

            person1_person2_diary = Diary.objects.filter(person1=this_person, person2=checkin_form.instance.with_who) \
                or Diary.objects.filter(person1=checkin_form.instance.with_who, person2=this_person)
            if not person1_person2_diary:
                Diary.objects.create(person1=request.user.person, person2=checkin_form.instance.with_who)

            this_person_settings = PersonalSettings.objects.get(person=this_person)
            if this_person_settings.display_periodical_notification:
                update_last_periodical_notification(request.user.person)

            return redirect('/diary/')
    csrf(request)
    return render(request, "checkin.html", locals())


def update_last_periodical_notification(person):
    this_person_notifications = PeriodicalNotification.objects.filter(person=person)
    last_entry = this_person_notifications.latest('date_saved')
    last_entry.date_saved = date.today()
    last_entry.save(update_fields=['date_saved'])
