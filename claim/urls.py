# -*- coding: utf-8 -*-
from django.views.static import *
from django.conf.urls import patterns, include, url
from claim.form import ClaimAuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('claim.views',
                       url(r'^internet_error_list/$', 'internet_error_list', name='internet_error_list'),
                       url(r'^claims_internet/$', 'claims_internet', name='claims_internet'),
                       url(r'^claims_update/(?P<id>.+)/$', 'claims_update', name='claims_update'),
                       url(r'^claim_delete/(?P<id>.+)/$', 'claim_delete', name='claim_delete'),
                       url(r'^statistics/claims_statistic_year/$', 'claims_statistic_year', name='claims_statistic_year'),
                       url(r'^statistics/claims_statistic_month/$', 'claims_statistic_month', name='claims_statistic_month'),
                       url(r'^statistics/claims_statistic_week/$', 'claims_statistic_week', name='claims_statistic_week'),
                       url(r'^statistics/claims_statistic_day/$', 'claims_statistic_day', name='claims_statistic_day'),
                       url(r'^statistics/$', 'internet_claims_statistic', name='internet_claims_statistic'),
                       url(r'^workers_internet_statistic/$', 'workers_internet_statistic_view', name='workers_internet_statistic'),
                       url(r'^claims_list/$', 'claims_list', name='claims_list'),
                       url(r'^claims_add/$', 'claims_add', name='claims_add'),
                       url(r'^$', 'index', name='index'),
)

urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^login/$', 'login',
                            {'template_name': 'login.html', 'authentication_form': ClaimAuthenticationForm},
                            name='login'),
                        url(r'^logout/$', 'logout', {'template_name': 'logged_out.html'}, name='logout'),
)