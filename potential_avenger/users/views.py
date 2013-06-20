from datetime import date


from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.context_processors import csrf
from django.contrib.auth import login


from users.models import Person, PersonPreferences, PersonalSettings
from users.forms import PersonForm, UserForm, PersonPreferencesForm, PersonalSettingsForm


@login_required
def profile(request):
    try:
        full_name = str(request.user.person)
    except User.DoesNotExist:
        fll_name = None
    try:
        email = request.user.email
    except User.DoesNotExist:
        email = None
    try:
        gender = request.user.person.get_gender_display()
    except Person.DoesNotExist:
        gender = None
    try:
        age = int((date.today() - request.user.person.birth_date).days/365)
    except Person.DoesNotExist:
        age = None
    try:
        city = request.user.person.city
    except Person.DoesNotExist:
        city = None
    try:
        preferred_poses = [str(pose) for pose in request.user.person.personpreferences.preferred_poses.all()]
    except PersonPreferences.DoesNotExist:
        preferred_poses = None
    try:
        preferred_places = [str(place) for place in request.user.person.personpreferences.preferred_places.all()]
    except PersonPreferences.DoesNotExist:
        preferred_places = None
    female_friends = User.objects.filter(person__gender='F').exclude(id=request.user.id)
    try:
        related_to = str(request.user.person.personpreferences.relation)
    except PersonPreferences.DoesNotExist:
        related_to = None
    try:
        profile_photo = request.user.person.photo.url
    except Person.DoesNotExist:
        profile_photo = '/media/profile_photos/noPhoto.jpg'
    useful_tips = request.user.person.personalsettings.useful_tips
    notification_period = request.user.person.personalsettings.notification_period
    return render(request, "profile.html", locals())


@login_required
def profile_edit(request):
    args = {}
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=request.user.person)
    user_form = UserForm(request.POST or None, instance=request.user)
    person_preferences_form = PersonPreferencesForm(request.POST or None, request.FILES or None, instance=request.user.person.personpreferences)
    personal_settings_form = PersonalSettingsForm(request.POST or None, request.FILES or None, instance=request.user.person.personalsettings)
    if request.method == 'POST':
        if person_form.is_valid() and user_form.is_valid() and person_preferences_form.is_valid() and personal_settings_form.is_valid():
            person_form.save()
            user_form.save()
            person_preferences_form.save()
            personal_settings_form.save()
            return redirect('/profile/')
    args.update(csrf(request))
    args['person_form'] = person_form
    args['user_form'] = user_form
    args['person_preferences_form'] = person_preferences_form
    args['personal_settings_form'] = personal_settings_form
    return render_to_response('profile_edit.html', args)


def login_user(request):
    args = {}
    authentication_form = AuthenticationForm(None, request.POST or None)
    if request.method == 'POST':
        if authentication_form.is_valid():
            user = authentication_form.get_user()
            login(request, user=user)
            return redirect('/profile/')
    args['authentication_form'] = authentication_form
    args.update(csrf(request))
    return render_to_response('login.html', args)


def register(request):
    args = {}
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = form.instance
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            created_person = Person(user=user)
            created_person.save()
            person_preferences = PersonPreferences(person=created_person)
            person_preferences.save()
            personal_settings = PersonalSettings(person=created_person)
            personal_settings.save()
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


@login_required
def home(request):
    return redirect('/profile/')
