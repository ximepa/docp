from django.conf.urls import patterns, include, url
from django.contrib.auth import login, logout


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from api import router

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tim.views.home', name='home'),
    # url(r'^tim/', include('tim.foo.urls')),
    url(r'^planning/', include('planning.urls', 'planning')),
    #url(r'^/login/$', login, {'template_name': 'login.html'},),
    url(r'^', include('manual.urls', 'manual')),
    url(r'^', include('claim.urls', 'claim')),



    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^router/$', router, name='router'),
    url(r'^router/api/$', router.api, name='api'),
)
