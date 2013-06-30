import random


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from hardcoded_models.models import PosesList, PlacesList


@login_required
def dice(request):
    random_pose = random.choice(PosesList.objects.all())
    random_place = random.choice(PlacesList.objects.all())
    return render(request, "dice.html", locals())
