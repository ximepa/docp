# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from claim.models import *
from options.models import Importance
from django.contrib import admin
from form import ChangeInternetWorkerForm, ChangeCtvWorkerForm, ChangeStatusForm, ChangeImportanceForm, ChangeClaims_groupForm
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, render
from daterange_filter.filter import DateRangeFilter
from django.contrib.admin.filters import RelatedFieldListFilter
from django.contrib import messages



# Internet
def change_claims_group(modeladmin, request, queryset):

    form = None

    if 'apply' in request.POST:
        form = ChangeClaims_groupForm(request.POST)

        if form.is_valid():
            importance = form.cleaned_data['importance']
            count = 0

            for item in queryset:

                item.importance = importance
                item.save()
                count += 1

            modeladmin.message_user(request, "Група %s встановлена в %d заявок" % (importance, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeClaims_groupForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'claims-internet/admin/change_claims_group_form.html', {'items': queryset, 'form': form, 'title': u'Змінити Групу'})

change_claims_group.short_description = u"Змінити важливість"


def set_importance(modeladmin, request, queryset):

    form = None

    if 'apply' in request.POST:
        form = ChangeImportanceForm(request.POST)

        if form.is_valid():
            importance = form.cleaned_data['importance']
            count = 0

            for item in queryset:

                item.importance = importance
                item.save()
                count += 1

            modeladmin.message_user(request, "Важливість %s встановлена в %d заявок" % (importance, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeImportanceForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'claims-internet/admin/set_importance_form.html', {'items': queryset, 'form': form, 'title': u'Змінити важливість'})

set_importance.short_description = u"Змінити важливість"


def change_internet_worker(modeladmin, request, queryset):

    form = None

    if 'apply' in request.POST:
       form = ChangeInternetWorkerForm(request.POST)

       if form.is_valid():
           who_do = form.cleaned_data['worker']

           count = 0
           for item in queryset:
               item.who_do = who_do
               item.save()
               count += 1

           modeladmin.message_user(request, "Працівник %s отримав %d заявок" % (who_do, count))
           return HttpResponseRedirect(request.get_full_path())

    if not form:
       form = ChangeInternetWorkerForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'claims-internet/admin/change_worker_form.html', {'items': queryset,'form': form, 'title':u'Змінити працівника'})

change_internet_worker.short_description = u"Змінити працівника"


def change_status(modeladmin, request, queryset):

    form = None

    if 'apply' in request.POST:
       form = ChangeStatusForm(request.POST)

       if form.is_valid():
           status = form.cleaned_data['status']
           what_do = form.cleaned_data['what_do']

           count = 0
           for item in queryset:
               item.status = status
               item.what_do = what_do
               item.save()
               count += 1

           modeladmin.message_user(request, "Заявки %s отримали %d заявок" % (status, count))
           return HttpResponseRedirect(request.get_full_path())

    if not form:
       form = ChangeStatusForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'claims-internet/admin/change_status_form.html', {'items': queryset,'form': form, 'title':u'Змінити статус'})

change_status.short_description = u"Змінити статус"


class ClaimsInternetFilter(RelatedFieldListFilter):

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(ClaimsInternetFilter, self).__init__(field, request, params, model, model_admin, field_path)
        workers = Worker.objects.filter(is_active=True, work_type__name__icontains='Інтернет')
        self.lookup_choices = [(w.id, w.name) for w in workers]


class ClaimInternetAdmin(admin.ModelAdmin):

    class Media:
        css = {
            "all": ("/static/css/ui-lightness/jquery-ui-1.10.3.custom.min.css", "/static/css/custom.css")
        }
        js = (
            "/static/js/jquery-1.7.2.min.js",
            "/static/js/jquery-ui-1.10.3.custom.min.js",
            "/static/js/jquery.util.js",
            "/static/js/jquery.form.js",
            "/static/js/jquery.rpc.js",
            "/router/api/",
            "/static/js/ajax-csrf.js",
            "/static/js/application.js",
            "/static/js/filter.js",
        )

    def save_model(self, request, obj, form, change):
        current_user = User.objects.get(username=request.user)
        if current_user.last_name and current_user.first_name:
            obj.who_give = '%s %s' % (current_user.last_name, current_user.first_name)
            try:
                print 'try'
                claim = ClaimInternet.objects.get(status = False, login = obj.login)
                print claim.login
                print 'claim.login'
                if obj.status == False and obj.login == claim.login and obj.vyl == claim.vyl:
                    print 'if'
                    print obj.status
                    print obj.login
                    obj.login = u'ВИДАЛІТЬ ЦЮ ЗЯВКУ'
                    messages.error(request, 'Така заявка уже існує і досі не виконана, будьте обачливі і видаліть непотрібку заявку')
            except ClaimInternet.DoesNotExist:
                print 'claim.DoesNotExist'
                pass
        if not current_user.last_name:
            obj.who_give = '%s' % (current_user.first_name,)
            print 2
        if not current_user.first_name:
            obj.who_give = '%s' % (current_user.last_name,)
            print 3
        if not current_user.last_name and not current_user.first_name:
            obj.who_give = 'Прізвище та імя не зазначено в профілі'
            print 4
        obj.save()
    save_model.allow_tags = True
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "who_do":
            kwargs["queryset"] = Worker.objects.filter(is_active=True, work_type__name__icontains='Інтернет')
        if db_field.name == "error":
            kwargs["queryset"] = Error.objects.filter(type__id=1)
        return super(ClaimInternetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        #print request.META['QUERY_STRING']
        if ('HTTP_REFERER' in request.META) and (request.META['HTTP_REFERER'].find('?') == -1) and (not request.GET.has_key('status__exact')):
        #if not request.GET.has_key('status__exact'):
            q = request.GET.copy()
            q['status__exact'] = 0
	    q['claims_group__id__exact'] = 1
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(ClaimInternetAdmin, self).changelist_view(request, extra_context=extra_context)


    fieldsets = [
        (u'Заявка:', {'fields': ('login', 'vyl', 'kv', 'error', 'domtel', 'mobtel', 'importance', 'claim_type', 'line_type', )}),
        ('vukonanya', {'fields': (('status', 'disclaimer'), 'who_do', 'what_do')}),
        ('comments', {'fields': ['comments']}),
        ('advanced', {'classes': ('collapse',), 'fields': ['claims_group']}),
    ]
    list_display = ('importance_vyl', 'importance_kv', 'login', 'importance_error', 'importance_who_give', 'pub_date', 'datetime_view', 'date_give_view', 'date_change', 'who_do', 'what_do', 'same_claim_view', 'line_type',)


    def same_claim_view(self, ClaimInternet):
        if ClaimInternet.same_claim >= 1:
            return ('<div align="center" id="same_zayavka" style="background-color: red"><span style="color: white">%s</span></div>' % (ClaimInternet.same_claim))
        else:
            return ('<div align="center">%s</div>' % (ClaimInternet.same_claim))

    same_claim_view.allow_tags = True
    same_claim_view.short_description = 'Схожі заявки'
    same_claim_view.admin_order_field = 'same_claim'

    def datetime_view(self, ClaimInternet):
        if ClaimInternet.status == False:
            return ('<span> - </span>')
        else:
            return ('<span>%s</span>' % (ClaimInternet.datetime))
    datetime_view.allow_tags = True
    datetime_view.short_description = 'Дата вик.'
    datetime_view.admin_order_field = 'datetime'

    def date_give_view(self, ClaimInternet):
        if ClaimInternet.who_do == None:
            return ('<span> - </span>')
        else:
            return ('<span>%s</span>' % (ClaimInternet.date_give))
    date_give_view.allow_tags = True
    date_give_view.short_description = 'Отримав'
    date_give_view.admin_order_field = 'date_give'

    def importance_vyl(self, ClaimInternet):
        if ClaimInternet.importance_id == 1:
            return '<span title="// %s // %s // %s">%s</span>' % (ClaimInternet.domtel, ClaimInternet.mobtel, ClaimInternet.comments.replace('"','&quot;').replace("'","&apos;"), ClaimInternet.vyl)
        if ClaimInternet.importance_id == 2:
            return '<span style="color: #008000;" title="// %s // %s // %s">%s</span>' % (ClaimInternet.domtel, ClaimInternet.mobtel, ClaimInternet.comments.replace('"','&quot;').replace("'","&apos;"), ClaimInternet.vyl)
        if ClaimInternet.importance_id == 3:
            return '<span style="color: #dc0000;" title="// %s // %s // %s">%s</span>' % (ClaimInternet.domtel, ClaimInternet.mobtel, ClaimInternet.comments.replace('"','&quot;').replace("'","&apos;"), ClaimInternet.vyl)
    importance_vyl.allow_tags = True
    importance_vyl.short_description = 'Вулиця'
    importance_vyl.admin_order_field = 'vyl'

    def importance_kv(self, ClaimInternet):
        if ClaimInternet.importance_id == 1:
            return '%s' % (ClaimInternet.kv)
        if ClaimInternet.importance_id == 2:
            return '<span style="color: #008000;">%s</span>' % (ClaimInternet.kv)
        if ClaimInternet.importance_id == 3:
            return '<span style="color: #dc0000;">%s</span>' % (ClaimInternet.kv)
        else:
            return '%s' % (ClaimInternet.kv)
    importance_kv.allow_tags = True
    importance_kv.short_description = 'Кв.'
    importance_kv.admin_order_field = 'kv'

    def importance_login(self, ClaimInternet):
        if ClaimInternet.importance_id == 1:
            return '%s' % (ClaimInternet.login)
        if ClaimInternet.importance_id == 2:
            return '<span style="color: #008000;">%s</span>' % (ClaimInternet.login)
        if ClaimInternet.importance_id == 3:
            return '<span style="color: #dc0000;">%s</span>' % (ClaimInternet.login)
        else:
            return '%s' % (ClaimInternet.login)
    importance_login.allow_tags = True
    importance_login.short_description = 'Логін'
    importance_login.admin_order_field = 'login'

    def importance_error(self, ClaimInternet):
        if ClaimInternet.importance_id == 1:
            return '%s' % (ClaimInternet.error)
        if ClaimInternet.importance_id == 2:
            return '<span style="color: #008000;">%s</span>' % (ClaimInternet.error)
        if ClaimInternet.importance_id == 3:
            return '<span style="color: #dc0000;">%s</span>' % (ClaimInternet.error)
        else:
            return '%s' % (ClaimInternet.error)
    importance_error.allow_tags = True
    importance_error.short_description = 'Помилка'
    importance_error.admin_order_field = 'error'

    def importance_who_give(self, ClaimInternet):
        if ClaimInternet.importance_id == 1:
            return '%s' % (ClaimInternet.who_give)
        if ClaimInternet.importance_id == 2:
            return '<span style="color: #008000;">%s</span>' % (ClaimInternet.who_give)
        if ClaimInternet.importance_id == 3:
            return '<span style="color: #dc0000;">%s</span>' % (ClaimInternet.who_give)
        else:
            return '%s' % (ClaimInternet.who_give)
    importance_who_give.allow_tags = True
    importance_who_give.short_description = 'Додав'
    importance_who_give.admin_order_field = 'who_give'

    radio_fields = {"importance": admin.HORIZONTAL, "claim_type": admin.HORIZONTAL, 'line_type': admin.HORIZONTAL}
    list_filter = ['status',
                   ('who_do', ClaimsInternetFilter),
                   'importance',
                   'claims_group',
                   ('pub_date', DateRangeFilter)]

    search_fields = ['vyl__sorting', 'kv', 'login', 'error__name', 'who_give', 'domtel', 'mobtel', 'who_do__name', 'what_do', 'importance__status_importance']
    save_on_top = True
    date_hierarchy = 'datetime'
    actions = [set_importance, change_internet_worker, change_status]

# Ctv


def change_ctv_worker(modeladmin, request, queryset):

    form = None

    if 'apply' in request.POST:
       form = ChangeCtvWorkerForm(request.POST)

       if form.is_valid():
           who_do = form.cleaned_data['worker']

           count = 0
           for item in queryset:
               item.who_do = who_do
               item.save()
               count += 1

           modeladmin.message_user(request, "Працівник %s отримав %d заявок" % (who_do, count))
           return HttpResponseRedirect(request.get_full_path())

    if not form:
       form = ChangeCtvWorkerForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'claims-internet/admin/change_worker_form.html', {'items': queryset,'form': form, 'title':u'Змінити працівника'})

change_ctv_worker.short_description = u"Змінити працівника"

# ctv


class ClaimsCtvFilter(RelatedFieldListFilter):

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(ClaimsCtvFilter, self).__init__(field, request, params, model, model_admin, field_path)
        workers = Worker.objects.filter(is_active=True, work_type__name__icontains='Кабельне')
        self.lookup_choices = [(w.id, w.name) for w in workers]


class ClaimCtvAdmin(admin.ModelAdmin):

    class Media:
        css = {
            "all": ("/static/css/ui-lightness/jquery-ui-1.10.3.custom.min.css", "/static/css/custom.css")
        }
        js = (
            "/static/js/filter.js",
            "/static/js/jquery-1.7.2.min.js",
            "/static/js/jquery-ui-1.10.3.custom.min.js",
            "/static/js/jquery.util.js",
            "/static/js/jquery.form.js",
            "/static/js/jquery.rpc.js",
            "/router/api/",
            "/static/js/ajax-csrf.js",
            "/static/js/application.js",
        )

    def save_model(self, request, obj, form, change):
        current_user = User.objects.get(username=request.user)
        if current_user.last_name and current_user.first_name:
            obj.who_give = '%s %s' % (current_user.last_name, current_user.first_name)
            print 1
        if not current_user.last_name:
            obj.who_give = '%s' % (current_user.first_name,)
            print 2
        if not current_user.first_name:
            obj.who_give = '%s' % (current_user.last_name,)
            print 3
        if not current_user.last_name and not current_user.first_name:
            obj.who_give = 'Прізвище та імя не зазначено в профілі'
            print 4
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "who_do":
            kwargs["queryset"] = Worker.objects.filter(is_active=True, work_type__name__icontains='Кабельне')
        if db_field.name == "error":
            kwargs["queryset"] = Error.objects.filter(type__id=2)
        return super(ClaimCtvAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #class Media:
    #    css = {
    #        "jquery": ("jquery/jquery-ui/css/ui-lightness/jquery-ui-1.9.2.custom.css",)
    #    }
    #    js = ("/static/js/blinking.js",)

    def changelist_view(self, request, extra_context=None):
        #print request.META['QUERY_STRING']
        if ('HTTP_REFERER' in request.META) and (request.META['HTTP_REFERER'].find('?') == -1) and (not request.GET.has_key('status__exact')):
        #if not request.GET.has_key('status__exact'):
            q = request.GET.copy()
            q['status__exact'] = 0
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(ClaimCtvAdmin,self).changelist_view(request, extra_context=extra_context)


    fieldsets = [
        ('zayavka:', {'fields': ('vyl', 'kv', 'error', 'domtel', 'mobtel', 'importance', 'group', )}),
        ('vukonanya', {'fields': ('status', 'who_do', 'what_do')}),
        ('comments', {'fields': ['comments']}),
    ]
    list_display = ('importance_vyl', 'importance_kv', 'importance_error', 'domtel', 'mobtel', 'importance_who_give', 'pub_date', 'datetime_view', 'date_give_view', 'date_change', 'who_do', 'what_do','same_claim_view', 'group',)


    def same_claim_view(self, Zayavka_ktb):
        if Zayavka_ktb.same_claim >= 1:
            return ('<div align="center" id="same_zayavka" style="background-color: red"><span style="color: white">%s</span></div>' % (Zayavka_ktb.same_claim))
        else:
            return ('<div align="center">%s</div>' % (Zayavka_ktb.same_claim))

    same_claim_view.allow_tags = True
    same_claim_view.short_description = 'Схожі заявки'
    same_claim_view.admin_order_field = 'same_zayavka'

    def datetime_view(self, ClaimCtv):
        if ClaimCtv.status == False:
            return ('<span> - </span>')
        else:
            return ('<span>%s</span>' % (ClaimCtv.datetime))
    datetime_view.allow_tags = True
    datetime_view.short_description = 'Дата вик.'
    datetime_view.admin_order_field = 'datetime'

    def date_give_view(self, ClaimCtv):
        if ClaimCtv.who_do == None:
            return ('<span> - </span>')
        else:
            return ('<span>%s</span>' % (ClaimCtv.date_give))
    date_give_view.allow_tags = True
    date_give_view.short_description = 'Отримав'
    date_give_view.admin_order_field = 'date_give'

    def importance_vyl(self, ClaimCtv):
        if ClaimCtv.importance_id == 1:
            return '<span title="%s">%s</span>' % (ClaimCtv.comments.replace('"','&quot;').replace("'","&apos;"), ClaimCtv.vyl)
        if ClaimCtv.importance_id == 2:
            return '<span style="color: #008000;" title="// %s // %s // %s">%s</span>' % (ClaimCtv.domtel, ClaimCtv.mobtel, ClaimCtv.comments.replace('"','&quot;').replace("'","&apos;"), ClaimCtv.vyl)
        if ClaimCtv.importance_id == 3:
            return '<span style="color: #dc0000;" title="// %s // %s // %s">%s</span>' % (ClaimCtv.domtel, ClaimCtv.mobtel, ClaimCtv.comments.replace('"','&quot;').replace("'","&apos;"), ClaimCtv.vyl)
    importance_vyl.allow_tags = True
    importance_vyl.short_description = 'Вулиця'
    importance_vyl.admin_order_field = 'vyl'

    def importance_kv(self, ClaimCtv):
        if ClaimCtv.importance_id == 1:
            return '%s' % (ClaimCtv.kv)
        if ClaimCtv.importance_id == 2:
            return '<span style="color: #008000;">%s</span>' % (ClaimCtv.kv)
        if ClaimCtv.importance_id == 3:
            return '<span style="color: #dc0000;">%s</span>' % (ClaimCtv.kv)
        else:
            return '%s' % (ClaimCtv.kv)
    importance_kv.allow_tags = True
    importance_kv.short_description = 'Кв.'
    importance_kv.admin_order_field = 'kv'

    def importance_error(self, ClaimCtv):
        if ClaimCtv.importance_id == 1:
            return '%s' % (ClaimCtv.error)
        if ClaimCtv.importance_id == 2:
            return '<span style="color: #008000;">%s</span>' % (ClaimCtv.error)
        if ClaimCtv.importance_id == 3:
            return '<span style="color: #dc0000;">%s</span>' % (ClaimCtv.error)
        else:
            return '%s' % (ClaimCtv.error)
    importance_error.allow_tags = True
    importance_error.short_description = 'Помилка'
    importance_error.admin_order_field = 'error'

    def importance_who_give(self, ClaimCtv):
        if ClaimCtv.importance_id == 1:
            return '%s' % (ClaimCtv.who_give)
        if ClaimCtv.importance_id == 2:
            return '<span style="color: #008000;">%s</span>' % (ClaimCtv.who_give)
        if ClaimCtv.importance_id == 3:
            return '<span style="color: #dc0000;">%s</span>' % (ClaimCtv.who_give)
        else:
            return '%s' % (ClaimCtv.who_give)
    importance_who_give.allow_tags = True
    importance_who_give.short_description = 'Додав'
    importance_who_give.admin_order_field = 'who_give'
    radio_fields = {"importance": admin.HORIZONTAL,}
    list_filter = ['status', ('who_do', ClaimsCtvFilter), 'group', ('pub_date', DateRangeFilter)]
    search_fields = ['vyl__sorting', 'kv', 'login', 'error__name', 'who_give', 'domtel', 'mobtel', 'who_do__name', 'what_do', 'type__name_type', 'importance__status_importance']
    save_on_top = True
    date_hierarchy = 'datetime'
    actions = [set_importance, change_ctv_worker, change_status]

class GroupAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('group_name',)
    list_filter = ['group_name',]
    fields = ('group_name',)
    class Media:
    #    css = {
    #        "all": ("my_styles.css",)
    #    }
        js = ("js/filter.js",)

admin.site.register(ClaimCtv, ClaimCtvAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(ClaimInternet, ClaimInternetAdmin)
admin.site.register(Importance)
admin.site.register(Vyl)
admin.site.register(House)
admin.site.register(Error)
admin.site.register(Error_type)
admin.site.register(Line_type)
