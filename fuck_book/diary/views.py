from collections import OrderedDict


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from diary.models import Diary


@login_required
def diary(request):
    checkins_by_diary = OrderedDict()
    diary_list = sorted(list(Diary.get_diaries_for_people(request.user.person).all()), key=lambda x: x.datetime_created, reverse=True)
    for diary in diary_list:
        checkins_by_diary[diary] = sorted(list(diary.checkins.all()), key=lambda x: x.datetime_created, reverse=True)
    return render(request, "diary.html", locals())
