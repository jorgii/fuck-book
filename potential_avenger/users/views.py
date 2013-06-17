from datetime import date


from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf


from users.models import Person


@login_required
def profile(request):
    print(request.user.person.photo)
    full_name = request.user.person.__str__()
    gender = request.user.person.get_gender_display()
    age = int((date.today() - request.user.person.birth_date).days/365)
    city = request.user.person.city

    female_friends = User.objects.filter(person__gender='F').exclude(id=request.user.id)
    friends = [person.first_name for person in User.objects.exclude(id=request.user.id)]
    profile_photo = request.user.person.photo.url
    return render(request, "profile.html", locals())


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            p = Person(user=form.instance)
            p.save()
            return redirect('/register_success/')
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    return render_to_response('register.html', args)


def register_success(request):
    
    return render_to_response('register_success.html')
