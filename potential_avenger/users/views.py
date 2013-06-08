from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def profile(request):
    return render(request, "profile.html", locals())
