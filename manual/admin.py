# -*- coding: utf-8 -*-
from manual.models import Manual
from manual.models import Manualgroup
from django.contrib import admin

from django import forms



class ManualAdminForm(forms.ModelForm):
    class Meta:
        pass


class ManualAdmin(admin.ModelAdmin):

    form = ManualAdminForm
    class Media:
        css = {
            "all": ( "/static/css/custom.css",)
        }
        js = (
            "/static/js/disable_descr.js",
        )

    def save_model(self, request, obj, form, change):
        if not change:
            #obj.url = 'http://192.168.33.120:8080/manual/%s/' % (Manual.pk)
            obj.author = request.user
        if obj.lock:
            o = Manual.objects.get(pk=obj.pk)
            o.lock = True
            o.save()
        else:
            obj.save()

    def url_view(self, object):
        return '<p>%s</p>' % (object.id)
    url_view.allow_tags = True
    url_view.short_description = 'Редактировать'
    
    def show_view(self, object):
        return '<a href="http://192.168.33.120:8080/manual/%s/">%s</a>' % (object.id, object.name)
    show_view.allow_tags = True
    show_view.short_description = 'Link'

    fieldsets = [
        ('Мануал:', {'fields': ('name' , 'description', 'lock', 'group', 'url')}),
        ]
    list_display = ('url_view', 'show_view', 'group', 'created', 'author',)
    list_display_links = ('url_view',)
    list_filter = ['group',]
    search_fields = ['name', 'group__name', 'description', 'author']
    save_on_top = True

admin.site.register(Manual, ManualAdmin)
admin.site.register(Manualgroup)
