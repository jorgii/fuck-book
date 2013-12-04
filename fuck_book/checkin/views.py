from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from checkin.models import CheckinDetails
from checkin.forms import CheckinForm
from notifications.models import PeriodicalNotification
from persons.models import Person
from diary.models import Diary


@login_required
def checkin(request):
    this_person = request.user.person
    current_checkin = CheckinDetails(creator=this_person)
    checkin_form = CheckinForm(request.POST or None, instance=current_checkin)

    if request.method == 'POST':
        if checkin_form.is_valid():
            checkin_form.save()

            attached_diary = Diary.get_diary_for_exact_people(*list(current_checkin.participants.all()))
            if attached_diary:
                attached_diary.add_checkins_to_diary(current_checkin)
            else:
                Diary.create(creator=current_checkin.creator, participants=list(current_checkin.participants.all()), checkins=current_checkin)

            this_person_settings = Person.objects.get(id=this_person.id)
            if this_person_settings.display_periodical_notification:
                update_last_periodical_notification(this_person)

            return redirect('/diary/')
    csrf(request)
    return render(request, "checkin.html", locals())


def update_last_periodical_notification(person):
    ''' Takes one parameter - the curren logged person
    Finds the last periodical notification this person got
    and updates the date_saved of this notification to the
    date of the new chekin made in this request.
    '''
    this_person_notifications = PeriodicalNotification.objects.filter(person=person)
    last_entry = this_person_notifications.latest('date_saved')
    last_entry.date_saved = date.today()
    last_entry.save(update_fields=['date_saved'])
