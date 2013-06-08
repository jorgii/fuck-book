from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def dice(request):
    return render(request, "dice.html", locals())
