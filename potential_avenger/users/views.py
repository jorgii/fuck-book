from datetime import date


from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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


def login_user(request):
    args = {}
    authentication_form = AuthenticationForm(None, request.POST or None)
    if request.method == 'POST':
        print('In post: ', authentication_form.errors)
        if authentication_form.is_valid():
            user = authentication_form.get_user()
            login(request, user=user)
            return redirect('/profile/')
    args['authentication_form'] = authentication_form
    args.update(csrf(request))
    print(authentication_form.errors)
    return render_to_response('login.html', args)


def register(request):
    args = {}
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = form.instance
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            p = Person(user=user)
            p.save()
            login(request, user)
            return redirect('/register_success/')
    args['form'] = form
    args.update(csrf(request))
    return render_to_response('register.html', args)


@login_required
def register_success(request):
    args = {}
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=request.user.person)
    user_form = UserForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if person_form.is_valid() and user_form.is_valid():
            person_form.save()
            user_form.save()
            return redirect('/profile/')
    args.update(csrf(request))
    args['person_form'] = person_form
    args['user_form'] = user_form
    return render_to_response('register_success.html', args)
