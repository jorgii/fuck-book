from datetime import date


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.context_processors import csrf
from django.contrib.auth import login


from users.models import Person, PersonPreferences, PersonalSettings
from users.forms import PersonForm, UserForm, PersonPreferencesForm, PersonalSettingsForm
from notifications.models import PeriodicalNotification, TipNotification, DifferenceNotification


@login_required
def profile(request, username):
    path = '/profile/' + username + '/'
    logged_user_name = str(request.user.person)
    user_to_display = User.objects.get(username=username)
    if user_to_display == request.user:
        logged_user_view = True
    else:
        logged_user_view = False
    try:
        full_name = str(user_to_display.person)
    except User.DoesNotExist:
        fll_name = None
    try:
        email = user_to_display.email
    except User.DoesNotExist:
        email = None
    try:
        gender = user_to_display.person.get_gender_display()
    except Person.DoesNotExist:
        gender = None
    try:
        age = int((date.today() - user_to_display.person.birth_date).days/365)
    except Person.DoesNotExist:
        age = None
    except TypeError:
        age = None
    try:
        city = user_to_display.person.city
    except Person.DoesNotExist:
        city = None
    try:
        preferred_poses = [str(pose) for pose in user_to_display.person.personpreferences.preferred_poses.all()]
    except PersonPreferences.DoesNotExist:
        preferred_poses = None
    try:
        preferred_places = [str(place) for place in user_to_display.person.personpreferences.preferred_places.all()]
    except PersonPreferences.DoesNotExist:
        preferred_places = None
    female_friends = User.objects.filter(person__gender='F').exclude(id=user_to_display.id)
    try:
        related_to = str(user_to_display.person.personpreferences.relation)
    except PersonPreferences.DoesNotExist:
        related_to = None
    try:
        profile_photo = user_to_display.person.photo.url
    except ValueError:
        profile_photo = '/media/profile_photos/noPhoto.jpg'
    return render(request, 'profile.html', locals())


@login_required
def profile_edit(request):
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=request.user.person)
    user_form = UserForm(request.POST or None, instance=request.user)
    person_preferences_form = PersonPreferencesForm(request.POST or None, instance=request.user.person.personpreferences)
    personal_settings_form = PersonalSettingsForm(request.POST or None, instance=request.user.person.personalsettings)
    if request.method == 'POST':
        if person_form.is_valid() and user_form.is_valid() and person_preferences_form.is_valid() and personal_settings_form.is_valid():
            person_form.save()
            user_form.save()
            person_preferences_form.save()
            personal_settings_form.save()
            return redirect('/profile/'+request.user.username+'/')
    csrf(request)
    return render(request, 'profile_edit.html', locals())


def login_user(request):
    authentication_form = AuthenticationForm(None, request.POST or None)
    if request.method == 'POST':
        if authentication_form.is_valid():
            user = authentication_form.get_user()
            login(request, user=user)
            return redirect('/profile/'+user.username)
    csrf(request)
    return render(request, 'login.html', locals())


def register(request):
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
    csrf(request)
    return render(request, 'register.html', locals())


@login_required
def register_success(request):
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=request.user.person)
    user_form = UserForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if person_form.is_valid() and user_form.is_valid():
            person_form.save()
            user_form.save()
            PeriodicalNotification.objects.create(
                person=request.user.person,
                message="Wellcome! Don't hesitate to make your first check in.")
            TipNotification.objects.create(
                person=request.user.person,
                message="Wellcome! Go to your profile settings if you don't want to get useful tips.")
            DifferenceNotification.objects.create(
                person=request.user.person,
                message="Wellcome! Once you're in a relation you'll start getting difference notifications.")
            return redirect('/profile/'+request.user.username+'/')
    csrf(request)
    return render(request, 'register_success.html', locals())


@login_required
def home(request):
    return redirect('/profile/'+request.user.username)
