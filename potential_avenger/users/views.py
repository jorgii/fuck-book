from datetime import date


from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth import login

from users.models import Person
from users.forms import PersonForm, UserForm


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
            user = form.instance
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            p = Person(user=user)
            p.save()
            login(request, user)
            return redirect('/register_success/')
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    return render_to_response('register.html', args)


@login_required
def register_success(request):
    if request.method == 'POST':
        person_form = PersonForm(request.POST, instance=request.user.person)
        user_form = UserForm(request.POST, instance=request.user)
        print('person_form errors:', person_form.errors)
        print('user_form errors:', user_form.errors)
        if person_form.is_valid() and user_form.is_valid():
            user_form.save()
            person_form.save()
            print('success')
            return redirect('/profile/')
    args = {}
    args.update(csrf(request))
    args['person_form'] = PersonForm(instance=request.user.person)
    args['user_form'] = UserForm(instance=request.user)
    return render_to_response('register_success.html', args)
