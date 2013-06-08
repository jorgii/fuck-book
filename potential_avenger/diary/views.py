from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def diary(request):
    return render(request, "diary.html", locals())
