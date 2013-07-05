import random


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from hardcoded_models.models import PosesList, PlacesList


@login_required
def dice(request):
    try:
        random_pose = random.choice(PosesList.objects.all())
    except IndexError:
        random_pose = "Sorry, no available poses to choose from."
    try:
        random_place = random.choice(PlacesList.objects.all())
    except IndexError:
        random_place = "Sorry, no available places to choose from."
    return render(request, "dice.html", locals())
