from collections import OrderedDict, Counter
from itertools import groupby

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf


from statistics.forms import StatisticsForm
from checkin.models import CheckinDetails


@login_required
def statistics(request):
    statistics_form = StatisticsForm(request.POST or None)
    if request.method == 'POST':
        if statistics_form.is_valid():
            checkins_grouped = get_checkins_grouped(person=request.user.person,
                                                    from_t=statistics_form.cleaned_data['from_t'],
                                                    to_t=statistics_form.cleaned_data['to_t'],
                                                    group_by=statistics_form.cleaned_data['base'])
            checkins_statistics = OrderedDict()
            for group, checkins in checkins_grouped.items():
                checkins_statistics[group] = Counter()
                checkins_statistics[group]['average_duration'] = average(*[float(x.duration) for x in checkins])
                for checkin in checkins:
                    checkins_statistics[group]['number_of_checkins'] += 1
            print(checkins_grouped)
            print('-------------')
            print(checkins_statistics)
            return render(request, "statistics.html", locals())
    csrf(request)
    return render(request, "statistics.html", locals())


def get_checkins_grouped(person, from_t, to_t, group_by):
    checkins_all = list(CheckinDetails.objects.filter(date_checked__gte=from_t,
                                                      date_checked__lte=to_t,
                                                      person=person))

    checkins_all.extend(CheckinDetails.objects.filter(date_checked__gte=from_t,
                                                      date_checked__lte=to_t,
                                                      with_who=person))
    checkins_all = sorted(checkins_all, key=lambda x: x.date_checked)
    checkins_grouped_dict = OrderedDict()
    if group_by == 'd':
        for day, checkins_grouped in groupby(checkins_all, key=lambda x: x.date_checked):
            checkins_grouped_dict[day] = list(checkins_grouped)
        return checkins_grouped_dict
    elif group_by == 'm':
        for day, checkins_grouped in groupby(checkins_all, key=lambda x: x.date_checked.month):
            checkins_grouped_dict[day] = list(checkins_grouped)
        return checkins_grouped_dict


def average(*args):
    return '{:.2f}'.format(sum(args) / len(args))
