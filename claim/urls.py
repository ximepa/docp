# -*- coding: utf-8 -*-
from django.views.static import *
from django.conf.urls import patterns, include, url
from claim.form import ClaimAuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('claim.views',
    url(r'^claims_internet/$', 'claims_internet', name='claims_internet'),
    url( r'^claims_list/$', 'claims_list', name = 'claims_list' ),
    url(r'^$', 'index', name='index'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html', 'authentication_form':ClaimAuthenticationForm}, name='login'),
    url(r'^logout/$', 'logout', {'template_name': 'logged_out.html'}, name='logout'),
)