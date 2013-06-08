from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import date


@login_required
def profile(request):
    print(request.user.person.photo)
    full_name = '{} {}'.format(request.user.first_name, request.user.last_name)
    gender = request.user.person.get_gender_display()
    age = int((date.today() - request.user.person.birth_date).days/365)
    city = request.user.person.city

    profile_photo = request.user.person.photo.name
    return render(request, "profile.html", locals())
