from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def checkin(request):
    return render(request, "checkin.html", locals())
