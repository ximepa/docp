# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from manual.models import Manual
from manual.forms import ManualFilterForm
from manual.models import Manualgroup
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.db.models import Q


@login_required(login_url='/admin/login/')
def main(request):
    if request.user.is_authenticated():
        sensor = False
        if request.method == 'GET':
            request.session['search'] = request.GET.get('search')
            search = request.session.get('search', request.session['search'])
            manual_list = Manual.objects.all()
            if search:
                sensor = True
                manual_list = manual_list.filter(Q(name__icontains=search) | Q(model__icontains=search) |
                                                     Q(description__icontains=search) | Q(group__name__icontains=search) |
                                                     Q(author__icontains=search)
                                                     )
            manual_list_groups = {}
            for manual in manual_list:
                if not manual.group in manual_list_groups:
                    manual_list_groups.update({
                        manual.group: []
                    })
                manual_list_groups[manual.group].append(manual)
        else:
            sensor = False
            return ReferenceError
        filter_form = ManualFilterForm()
        return render_to_response('manual_list.html', {
            'user': request.user,
            'manual_list_groups': manual_list_groups,
            'filter_form': filter_form,
            'sensor': sensor,
            })
    else:
        error = 'Ви не авторизированы'
        return render_to_response('manual_list.html', {'user': request.user, 'error' : error,})

@login_required(login_url='/admin/login/')
def manual_full(request, id):
    manual = Manual.objects.get(id=id)
    if request.user.is_authenticated():
        return render_to_response('manual.html', {'user': request.user, 'manual' : manual,})
    else:
        error = 'Ви не авторизированы'
        return render_to_response('manual.html', {'user': request.user, 'error' : error,})


@login_required(login_url='/admin/login/')
def manual_count(request, id):
    manual = Manual.objects.all().count()
    if request.user.is_authenticated():
        return render_to_response('index.html', {'user': request.user, 'manual' : manual,})
    else:
        error = 'Ви не авторизированы'
        return render_to_response('index.html', {'user': request.user, 'error' : error,})