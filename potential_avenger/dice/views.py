from random import randint


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from hardcoded_models.models import PosesList, PlacesList


#@login_required
def dice(request):
    poses_counter = PosesList.objects.count() - 1
    print(poses_counter)
    index_poses = randint(0, poses_counter)
    print(index_poses)
    random_pose = PosesList.objects.all()[index_poses]
    places_counter = PlacesList.objects.count() - 1
    print(places_counter)
    index_places = randint(0, places_counter)
    print(index_places)
    random_place = PlacesList.objects.all()[index_places]
    return render(request, "dice.html", locals())
