from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def statistics(request):
    return render(request, "statistics.html", locals())
