from random import randint

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from models.hardcoded_models import NotificationType, TipsList


@login_required
def notifications(request):
    if NotificationType.notification_type == "periodical":
        message = "Haven't checked-in in a while. Sex life getting slow?"
    elif NotificationType.notification_type == "tip":
        tips_counter = TipsList.objects.count() - 1
        index_tips = randint(0, tips_counter)
        message = TipsList.objects.all()[index_tips]
    elif NotificationType.notification_type == "difference":
        message = ""
    else:
        raise NotificationType.NameError
    return render(request, "notifications.html", locals())
