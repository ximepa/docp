# -*- coding: utf-8 -*-
from django.views.static import *
from django.conf.urls import patterns, include, url
from claim.form import ClaimAuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('manual.views',
    url(r'^manual/(?P<id>.+)/$', 'manual_full', name='manual_full'),
    url(r'^manual/$', 'main', name='main'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html', 'authentication_form':ClaimAuthenticationForm}, name='login'),
    url(r'^logout/$', 'logout', {'template_name': 'logged_out.html'}, name='logout'),
)
