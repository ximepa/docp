# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from claim.models import ClaimInternet
from claim.lib import SortHeaders
from claim.form import InternetFilterForm
from django.shortcuts import render
from django.db.models import Q
from django.db.models import F
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
    if request.method == 'GET':
        request.session['status'] = request.GET.get('status', 0)
        status = request.session.get('status', request.session.get('status', 0))
        request.session['worker'] = request.GET.get('worker', None)
        worker = request.session.get('worker', request.session['worker'])
        request.session['search'] = request.GET.get('search')
        search = request.session.get('search', request.session['search'])
        request.session['ot'] = request.GET.get('ot')
        ot = request.session.get('ot', request.session['ot'])
        request.session['o'] = request.GET.get('o')
        o = request.session.get('o', request.session['o'])

    getparams_headers = request.GET.copy()
    getparams_headers.pop('ot', None)
    getparams_headers.pop('o', None)
    sort_headers = SortHeaders(request, LIST_HEADERS, default_order_field=6, default_order_type='desc', additional_params=getparams_headers.dict())
    claims_list = ClaimInternet.objects.all().order_by(sort_headers.get_order_by())
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
                        'ot': request.session['ot'],
                        'o':request.session['o'],
                        'search': request.GET.get('search'),
                        'status': request.session['status'],
                        'worker': request.session['worker'],
                        'claims_count': claims_list.count(),
                        'headers': list(sort_headers.headers()),
                        'user': request.user,
                        'filter_form': filter_form,
                    })

def actions(request, value, id):
    if request.method == "post":
        value = request.POST.get('value')
        claims_id_list = request.POST.getlist('id')


#def ajax_claims_search(request):
#    if request.is_ajax():
#        search = request.GET.get( 'search' )
#        print search
#        if search is not None:
#            claims = ClaimInternet.objects.filter(
#                Q( vyl = search ) |
#                Q( kv = search ) |
#                Q( login = search ) ).order_by( '-pub_date' )
#            data = {
#                'claims': claims,
#            }
#            return render_to_response( 'claims-internet/search_results.html', data,
#                                       context_instance = RequestContext( request ) )