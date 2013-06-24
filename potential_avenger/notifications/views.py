from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from models.hardcoded_models import TipsList


@login_required
def notifications(request):
    return render(request, "notifications.html", locals())
