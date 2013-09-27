# -*- coding: utf-8 -*-
from django.views.static import *
from django.conf.urls import patterns, include, url
from claim.form import ClaimAuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('planning.views',
    #url(r'^claims_internet/$', 'claims_internet', name='claims_internet'),
    url(r'^$', 'index', name='index'),
)