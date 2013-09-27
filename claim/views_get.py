# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from claim.models import ClaimInternet
from claim.lib import SortHeaders
from claim.form import InternetFilter
from django.db.models import Q
import datetime


@login_required(login_url='/login/')
def index(request):
    claim_internet_count_sf = ClaimInternet.objects.all().filter(status=False).count()
    claim_internet_count_st = ClaimInternet.objects.all().filter(status=True).count()
    claim_internet_count_all = ClaimInternet.objects.all().count()
    if request.user.is_authenticated():
        main_page = 'Hello'
        return render_to_response('index.html', {
                        'main': main_page,
                        'user': request.user,
                        'claim_internet_count_sf': claim_internet_count_sf,
                        'claim_internet_count_st': claim_internet_count_st,
                        'claim_internet_count_all': claim_internet_count_all,
                    }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def logout(request):
    logout(request)
    return HttpResponseRedirect('/')


LIST_HEADERS = (
    ('id', 'id'),
    ('Вулиця', 'vyl'),
    ('Кв', 'kv'),
    ('Логін', 'login'),
    ('Помилка', 'error'),
    ('Додав', 'who_give'),
    ('Дата створення', 'pub_date'),
    ('Дата виконання', 'datetime'),
    ('Отримав', 'date_give'),
    ('Різниця', 'date_change'),
    ('Виконавець', 'who_do'),
    #('Роботи', 'what_do'),
    ('Схожі заявки', 'same_claim'),
    ('Тип лінії', 'line_type'),
    ('Дії', 'status'),
)



def claims_internet(request):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    if request.method == 'GET':
        status_form = InternetFilter(request.GET)
        status = request.GET.get('status', '0')
        worker = request.GET.getlist('worker[]') or request.GET.get('worker')
        print '---------'
        print worker
        print '---------'
        # request.session['status'] = status

    else:
        status_form = InternetFilter()

    page = request.GET.get('page')
    getparams_page = request.GET.copy()
    getparams_page.pop('page', None)
    getparams_headers = request.GET.copy()
    getparams_headers.pop('ot', None)
    getparams_headers.pop('o', None)

    sort_headers = SortHeaders(request, LIST_HEADERS, default_order_field=6, default_order_type='desc',additional_params=getparams_headers.dict())
    claims_list = ClaimInternet.objects.all().order_by(sort_headers.get_order_by())
    if not status == 'None':
        claims_list = claims_list.filter(Q(status=status))
    if worker:
        print worker
        claims_list = claims_list.filter(Q(who_do__in=worker))
    paginator = Paginator(claims_list, 2) # Show 25 contacts per page

    try:
        claims = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        claims = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        claims = paginator.page(paginator.num_pages)
    headers = list(sort_headers.headers())
    return render_to_response('claims-internet/claims-list.html', {
                        'claims': claims,
                        'claims_count': claims_list.count(),
                        'getparams_page': getparams_page.urlencode(),
                        'headers': headers,
                        'user': request.user,
                        'status_form': status_form,
                    }, context_instance=RequestContext(request))


def load_json(request):
    """
    Event object format json

    [
      {
        "id": "2",
        "start": "2013-02-01 08:10:00",
        "end": "2013-02-01 11:00:00",
        "title": "French Open"
      },
      {
        "id": "97",
        "start": "2013-02-05",
        "allDay": true,
        "title": "FOOBAR Open",
        "url": "http:\/\/google.com"
      },
      {
        "id": "3",
        "start": "2013-02-03",
        "title": "Aegon Championship",
        "url": "http:\/\/google.com"
      }
    ]

    """

    # start/end dates are passed in from calendar widget
    try:
        start_timestamp = int(request.GET.get('start', False))
        end_timestamp = int(request.GET.get('end', False))
        date_give = datetime.datetime.fromtimestamp(start_timestamp)
        date_time = datetime.datetime.fromtimestamp(end_timestamp)
    except ValueError:
        date_give = datetime.date.today()
        date_time = datetime.datetime.today() + datetime.timedelta(days=7)

    # events schedule during the current active month
    event_list = ClaimInternet.objects.filter(date_give__gte=date_give,).filter(
        datetime__lt=date_time)

    s = '['

    for event in event_list:
        s += '{ "id": "%d",' % (event.id, )
        s +=' "title": "%s",' % (event.summary,)
        if event.all_day:
            s += ' "allDay":"true", "start":"%s",' % (event.start_date,)
        else:
            s += ' "start":"%s %s", "end": "%s %s",' % (event.start_date, event.start_time, event.end_date, event.end_time)
        s += ' "backgroundColor":"%s",' % (event.color, )
        s +=' "url": "/calendar/event/%d/update/" }' %  (event.id,)
        if not event == event_list[event_list.count()-1]:
            s += ','

    s+= ']'

    return HttpResponse(s, content_type="application/json")