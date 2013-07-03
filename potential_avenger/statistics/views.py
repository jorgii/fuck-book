from collections import OrderedDict, Counter
from itertools import groupby

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from statistics.forms import StatisticsForm
from checkin.models import CheckinDetails


@login_required
def statistics(request):
    checkins_statistics = list()
    statistics_form = StatisticsForm(request.GET or None)
    if statistics_form.is_valid():
        group_by = statistics_form.cleaned_data['base']
        checkins_grouped = get_checkins_grouped(person=request.user.person,
                                                from_t=statistics_form.cleaned_data['from_t'],
                                                to_t=statistics_form.cleaned_data['to_t'],
                                                group_by=group_by)
        index = 0
        for group, checkins in checkins_grouped.items():
            checkins_statistics.append(Counter())
            partners = []
            places = []
            poses = []
            number_with_contraception = 0
            number_without_contraception = 0
            for checkin in checkins:
                checkins_statistics[index]['number_of_checkins'] += 1
                for pose in checkin.poses.all():
                    poses.append(pose)
                for place in checkin.places.all():
                    places.append(place)
                if request.user.person == checkin.with_who and checkin.person:
                    partners.append(checkin.person)
                elif request.user.person == checkin.person and checkin.with_who:
                    partners.append(checkin.with_who)
                if checkin.contraception:
                    number_with_contraception += 1
                else:
                    number_without_contraception += 1
            checkins_statistics[index]['date'] = group
            checkins_statistics[index]['average_duration'] = average(*[float(x.duration) for x in checkins])
            checkins_statistics[index]['average_rating'] = average(*[float(x.rating) for x in checkins])
            checkins_statistics[index]['top_three_partners'] = get_top_three(*partners)
            checkins_statistics[index]['top_three_places'] = get_top_three(*places)
            checkins_statistics[index]['top_three_poses'] = get_top_three(*poses)
            checkins_statistics[index]['contraception'] = number_with_contraception
            checkins_statistics[index]['no_contraception'] = number_without_contraception
            index += 1
    paginator = Paginator(checkins_statistics, 4)
    page = request.GET.get('page')
    try:
        statistics_page = paginator.page(page)
    except PageNotAnInteger:
        statistics_page = paginator.page(number=1)
    except EmptyPage:
        statistics_page = paginator.page(paginator.num_pages)
    return render(request, "statistics.html", locals())


def get_checkins_grouped(person, from_t, to_t, group_by):
    checkins_all = list(CheckinDetails.objects.filter(date_checked__gte=from_t,
                                                      date_checked__lte=to_t,
                                                      person=person))

    checkins_all.extend(CheckinDetails.objects.filter(date_checked__gte=from_t,
                                                      date_checked__lte=to_t,
                                                      with_who=person))
    checkins_all = sorted(checkins_all, key=lambda x: x.date_checked, reverse=True)
    checkins_grouped_dict = OrderedDict()
    if group_by == 'd':
        for day, checkins_grouped in groupby(checkins_all, key=lambda x: x.date_checked):
            checkins_grouped_dict[day] = list(checkins_grouped)
    elif group_by == 'm':
        for month, checkins_grouped in groupby(checkins_all, key=lambda x: str(x.date_checked.month) + '/' + str(x.date_checked.year)):
            checkins_grouped_dict[month] = list(checkins_grouped)
    return checkins_grouped_dict


def average(*args):
    return '{:.2f}'.format(sum(args) / len(args))


def get_top_three(*args):
    '''
    Returns most common three elements in given list or arguments.
    '''
    top_three = [x[0] for x in Counter(args).most_common(3)]
    return top_three
