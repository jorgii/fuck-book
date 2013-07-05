from collections import OrderedDict


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from diary.models import Diary
from checkin.models import CheckinDetails


@login_required
def diary(request):
    checkins_by_diary = OrderedDict()
    diary_list = list(Diary.objects.filter(person1=request.user.person))
    diary_list.extend(list(Diary.objects.filter(person2=request.user.person)))
    diary_list = sorted(diary_list, key=lambda x: x.timestamp, reverse=True)
    for diary in diary_list:
        checkins_by_diary[diary] = get_checkins_for_diary(diary)
    return render(request, "diary.html", locals())


def get_checkins_for_diary(diary):
    '''Takes a diary as a parameter and returns all checkins connected to this diary.
    Gathers all checkins with person1 and person2 or person2 and person1.

    '''
    checkins = list(CheckinDetails.objects.filter(person=diary.person1,
                                                  with_who=diary.person2))
    checkins.extend(CheckinDetails.objects.filter(person=diary.person2,
                                                  with_who=diary.person1))
    return sorted(checkins, key=lambda x: x.date_checked, reverse=True)
