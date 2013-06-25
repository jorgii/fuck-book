from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from diary.models import Diary


@login_required
def diary(request):
    diary_list = Diary.objects.filter(person1=request.user.person)
    persons_list = []
    for diary in diary_list:
        persons_list.append([str(diary.person1), str(diary.person2)])
    return render(request, "diary.html", locals())
