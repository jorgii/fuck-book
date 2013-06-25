from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from checkin.forms import CheckinForm


@login_required
def checkin(request):
    checkin_form = CheckinForm(request.POST or None)
    if request.method == 'POST':
        if checkin_form.is_valid():
            checkin_form.save()
            return redirect('/diary/')
    csrf(request)
    return render(request, "checkin.html", locals())
