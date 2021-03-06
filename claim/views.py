# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from claim.models import ClaimInternet
from options.models import Error, Dom, Worker
from claim.lib import SortHeaders
from claim.form import InternetFilterForm
from django.shortcuts import render
from django.db.models import Q
from django.db.models import F
from datetime import timedelta
from django.utils import timezone
import datetime
import json


@login_required(login_url='/login/')
def index(request):
    claim_internet_count_sf = ClaimInternet.objects.all().filter(status=False).count()
    claim_internet_count_st = ClaimInternet.objects.all().filter(status=True).count()
    claim_internet_count_all = ClaimInternet.objects.all().count()
    if request.user.is_authenticated():
        return render_to_response('index.html', {
                        'user': request.user,
                        'claim_internet_count_sf': claim_internet_count_sf,
                        'claim_internet_count_st': claim_internet_count_st,
                        'claim_internet_count_all': claim_internet_count_all,
                    }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def internet_claims_statistic(request):
    if request.user.is_authenticated():
        return render_to_response('internet_claims_statistic.html', {
                        'user': request.user,
                    }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def workers_internet_statistic_view(request):
    if request.user.is_authenticated():
        workers = Worker.objects.filter(work_type__name__icontains='Інтернет', show_in_graphs=True)
        return render_to_response('workers_inet_stats.html', {
                        'user': request.user,
                        'workers': workers,
                    }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


# def logout(request):
#     logout(request)
#     return HttpResponseRedirect('/')


LIST_HEADERS = (
    ('Вулиця', 'vyl'),
    ('Кв.', 'kv'),
    ('Логін', 'login'),
    ('Помилка', 'error'),
    ('Додав', 'who_give'),
    ('Створена', 'pub_date'),
    ('Виконана', 'datetime'),
    ('Отримав', 'date_give'),
    ('Виконавець', 'who_do'),
    ('Схожі', 'same_claim'),
    ('Лінія', 'line_type'),
    ('Дії', 'status'),
)


def claims_internet(request):
    order_by = request.GET.get('order_by', '-pub_date')
    if request.method == 'GET':
        request.session['status'] = request.GET.get('status', 0)
        status = request.session.get('status', request.session.get('status', 0))
        request.session['worker'] = request.GET.get('worker', None)
        worker = request.session.get('worker', request.session['worker'])
        request.session['search'] = request.GET.get('search')
        search = request.session.get('search', request.session['search'])
    claims_list = ClaimInternet.objects.all().order_by(order_by)
    if not status == 'None':
        claims_list = claims_list.filter(Q(status=status))
    if worker:
        claims_list = claims_list.filter(Q(who_do__id=worker))
    if search:
        claims_list = claims_list.filter(Q(vyl__sorting__icontains=search) | Q(kv__icontains=search) |
                                         Q(login__icontains=search) | Q(who_give__icontains=search) |
                                         Q(who_do__name__icontains=search) | Q(line_type__name__icontains=search) |
                                         Q(error__name__icontains=search)
                                         )
    print claims_list.count()
    paginator = Paginator(claims_list, 50) # Show 25 contacts per page
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        claims = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        claims = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        claims = paginator.page(paginator.num_pages)
    filter_form = InternetFilterForm(initial={'status': status, 'worker': worker})
    return render(request, 'claims-internet/claims-list.html', {
                        'claims': claims,
                        'search': request.GET.get('search'),
                        'status': status,
                        'worker': request.session['worker'],
                        'claims_count': claims_list.count(),
                        'user': request.user,
                        'filter_form': filter_form,
                    })

def default(obj):
    """Default JSON serializer."""
    import calendar, datetime

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    millis = int(
        calendar.timegm(obj.timetuple()) * 1000 +
        obj.microsecond / 1000
    )
    return millis


def claims_list(request):
    if request.is_ajax():
        data = None
        status = request.GET.get('status')
        disclaim = request.GET.get('disclaim')
        search = request.GET.get('search')
        claims = ClaimInternet.objects.all()
        if status and disclaim and search:
            claims = ClaimInternet.objects.filter(
                Q(status=status, disclaimer=disclaim, login__icontains=search))
        elif status and disclaim:
            claims = ClaimInternet.objects.filter(
                Q(status=status, disclaimer=disclaim,))
        elif status and search:
            claims = ClaimInternet.objects.filter(
                Q(status=status, login__icontains=search,))
        elif status:
            claims = ClaimInternet.objects.filter(
                Q(status=status,))
        elif disclaim and search:
            claims = ClaimInternet.objects.filter(
                Q(disclaimer=disclaim, login__icontains=search))
        elif disclaim:
            claims = ClaimInternet.objects.filter(
                Q(disclaimer=disclaim,))
        elif search:
            claims = ClaimInternet.objects.filter(
                Q(login__icontains=search))
        data = [{
                'claim_id': c.id,
                'claim_vyl': c.vyl.sorting,
                'claim_kv': c.kv,
                'claim_login': c.login,
                'claim_status': c.status,
                'claim_disclaimer': c.disclaimer,
                'claim_error': c.error.name,
                'claim_who_give': c.who_give,
                'claim_pub_date': json.dumps(c.pub_date, default=default),
                'claim_importance': c.importance.status_importance,
                'claim_claim_type': c.claim_type.name,
                'claim_line_type': c.line_type.name
            } for c in claims]
        return HttpResponse(json.dumps(data))

def parseBoolString(theString):
    return theString[0].upper() == 'T'

def claims_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            claims = ClaimInternet.objects.all().order_by('-pub_date')
            print request.POST.get('claim_vyl'),
            print request.POST.get('claim_kv'),
            print request.POST.get('claim_login'),
            print parseBoolString(request.POST.get('claim_status')),
            print parseBoolString(request.POST.get('claim_disclaimer')),
            print request.POST.get('claim_error'),
            cm = ClaimInternet(
                vyl_id=request.POST.get('claim_vyl'),
                kv=request.POST.get('claim_kv'),
                login=request.POST.get('claim_login'),
                who_give=request.user.last_name + ' ' + request.user.first_name,
                status=parseBoolString(request.POST.get('claim_status')),
                disclaimer=parseBoolString(request.POST.get('claim_disclaimer')),
                error_id=request.POST.get('claim_error'),
                pub_date = datetime.datetime.now(),
                datetime=datetime.datetime.now(),
                date_change=None,
                date_give=datetime.datetime.now(),
            )
            cm.save()
            data = [{
                'claim_id': c.id,
                'claim_vyl': c.vyl.sorting,
                'claim_kv': c.kv,
                'claim_login': c.login,
                'claim_status': c.status,
                'claim_disclaimer': c.disclaimer,
                'claim_error': c.error.name,
                'claim_who_give': c.who_give,
                'claim_pub_date': json.dumps(c.pub_date, default=default),
                'claim_importance': c.importance.status_importance,
                'claim_claim_type': c.claim_type.name,
                'claim_line_type': c.line_type.name
            } for c in claims]
    return HttpResponse(json.dumps(data))


def claims_update(request, id):
    if request.is_ajax():
        if request.method == 'POST':
            claim = ClaimInternet.objects.get(id=id)
            data = [{
                'claim_vyl': claim.vyl_id,
                'claim_kv': claim.kv,
                'claim_login': claim.login,
                'claim_status': claim.status,
                'claim_disclaimer': claim.disclaimer,
            }]
            return HttpResponse(json.dumps(data))


def claim_delete(request, id):
    if request.is_ajax():
        if request.method == 'POST':
            claim = ClaimInternet.objects.get(id=id)
            claim.delete()
            return HttpResponse("OK")



def internet_error_list(request):
    if request.is_ajax():
        errors = Error.objects.all().order_by('name').filter(type=1)
        error_data = [{
            'error_id': e.id,
            'error_name': e.name,
         } for e in errors]
        return HttpResponse(json.dumps(error_data))


def claims_statistic_year(request):
    today_year = datetime.date.today().year
    if request.is_ajax():
        year_list = ClaimInternet.objects.filter(pub_date__year=today_year).dates('pub_date', 'day')
        data = [{
            'year': str(years.year) + '-' + str(years.month) + '-' + str(years.day),
            'claims_all_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day).count(),
            'claims_completed_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, status=True,).count(),
            'claims_disclaim_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, disclaimer=True,).count(),
            'claims_uncompleted_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, disclaimer=False, status=False, claims_group=1).count(),
            'claims_given_to_plumber_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, disclaimer=False, status=False, claims_group=2).count(),
         } for years in year_list]
        return HttpResponse(json.dumps(data))


def claims_statistic_month(request):
    today_year = datetime.date.today().year
    today_month = datetime.date.today().month
    if request.is_ajax():
        month_list = ClaimInternet.objects.filter(pub_date__year=today_year, pub_date__month=today_month).dates('pub_date', 'day')
        data = [{
            'month': str(years.year) + '-' + str(years.month) + '-' + str(years.day),
            'claims_all_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day).count(),
            'claims_completed_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, status=True,).count(),
            'claims_disclaim_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, disclaimer=True,).count(),
            'claims_uncompleted_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, disclaimer=False, status=False, claims_group=1).count(),
            'claims_given_to_plumber_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, disclaimer=False, status=False, claims_group=2).count(),
         } for years in month_list]
        return HttpResponse(json.dumps(data))


def claims_statistic_week(request):
    if request.is_ajax():
        day_last_week = timezone.now().date() - timedelta(days=7)
        day_this_week = day_last_week + timedelta(days=8)
        month_list = ClaimInternet.objects.filter(pub_date__gte=day_last_week, pub_date__lte=day_this_week).dates('pub_date', 'day')
        data = [{
            'week': str(years.year) + '-' + str(years.month) + '-' + str(years.day),
            'claims_all_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day).count(),
            'claims_completed_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, status=True,).count(),
            'claims_disclaim_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, disclaimer=True,).count(),
            'claims_uncompleted_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, disclaimer=False, status=False, claims_group=1).count(),
            'claims_given_to_plumber_count': ClaimInternet.objects.filter(pub_date__year=years.year, pub_date__month=years.month, pub_date__day=years.day, disclaimer=False, status=False, claims_group=2).count(),
         } for years in month_list]
        return HttpResponse(json.dumps(data))


def claims_statistic_day(request):
    if request.is_ajax():
        today_year = datetime.date.today().year
        today_month = datetime.date.today().month
        today_day = datetime.date.today().day
        data = [{
            'day': str(today_year) + '-' + str(today_month) + '-' + str(today_day),
            'claims_uncompleted_count': ClaimInternet.objects.filter(disclaimer=False, status=False, claims_group=1).count(),
            'claims_given_to_plumber_count': ClaimInternet.objects.filter(disclaimer=False, status=False, claims_group=2).count(),
         }]
        return HttpResponse(json.dumps(data))
