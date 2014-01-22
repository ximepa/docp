# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from claim.models import *
from options.models import Importance
from django.contrib import admin
from .form import ChangeInternetWorkerForm, ChangeCtvWorkerForm, ChangeStatusForm, ChangeImportanceForm, ChangeClaims_groupForm
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, render
from daterange_filter.filter import DateRangeFilter
from django.contrib.admin.filters import RelatedFieldListFilter
from django.contrib import messages
#from django.conf.urls.defaults import patterns
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q



# internet
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
            disclaimer = form.cleaned_data['disclaimer']
            what_do = form.cleaned_data['what_do']

            count = 0
            for item in queryset:
               item.status = status
               item.what_do = what_do
               item.disclaimer = disclaimer
               item.save()
               count += 1

            modeladmin.message_user(request, "Статус %s отримали %d заявок" % (status, count))
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
            "/static/js/bootstrap.min.js",
        )

    def format_pub_date(self, obj):
        return obj.pub_date.strftime('%Y-%m-%d %H:%M')
    format_pub_date.short_description = 'Дата створення'
    format_pub_date.admin_order_field = 'pub_date'

    def save_model(self, request, obj, form, change):
        current_user = User.objects.get(username=request.user)
        if obj.who_give == '':
            not_do_claim = ClaimInternet.objects.filter(disclaimer = 0, status=0, login=obj.login)
            for claim in not_do_claim:
                if claim.login == obj.login:
                    same_claim = 'Така заявка вже існує %s' % claim.pk
                    messages.add_message(request, messages.ERROR, same_claim)
                    return obj
            if current_user.last_name and current_user.first_name:
                obj.who_give = '%s %s' % (current_user.last_name, current_user.first_name)
            if not current_user.last_name:
                obj.who_give = '%s' % (current_user.first_name,)
            if not current_user.first_name:
                obj.who_give = '%s' % (current_user.last_name,)
            if not current_user.last_name and not current_user.first_name:
                obj.who_give = 'Прізвище та імя не зазначено в профілі'
        else:
            obj.who_give = obj.who_give
        obj.save()
        messages.add_message(request, messages.INFO, 'Не забудь сказати номер заявки')
    save_model.allow_tags = True
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "who_do":
            kwargs["queryset"] = Worker.objects.filter(is_active=True, work_type__name__icontains='Інтернет')
        if db_field.name == "error":
            kwargs["queryset"] = Error.objects.filter(type__id=1)
        return super(ClaimInternetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        try:
            test = request.META['HTTP_REFERER'].split(request.META['PATH_INFO'])
            if test and test[-1] and not test[-1].startswith('?') and not request.GET.has_key('status__exact') and not request.GET.has_key('claims_group__id__exact') and not request.GET.has_key('disclaimer__exact'):
                return HttpResponseRedirect("/admin/claim/claiminternet/?claims_group__id__exact=1&disclaimer__exact=0&status__exact=0")
        except: pass # In case there is no referer
        return super(ClaimInternetAdmin,self).changelist_view(request, extra_context=extra_context)

    # def changelist_view(self, request, extra_context=None):
    #     #print request.META['QUERY_STRING']
    #     if ('HTTP_REFERER' in request.META) and (request.META['HTTP_REFERER'].find('?') == -1) and (not request.GET.has_key('status__exact')):
    #     #if not request.GET.has_key('status__exact'):
    #         q = request.GET.copy()
    #         q['status__exact'] = 0
    #         q['disclaimer__exact'] = 0
	 #    q['claims_group__id__exact'] = 1
    #         request.GET = q
    #         request.META['QUERY_STRING'] = request.GET.urlencode()
    #     return super(ClaimInternetAdmin, self).changelist_view(request, extra_context=extra_context)


    fieldsets = [
        (u'Заявка:', {'fields': ('login', 'vyl', 'kv', 'error', 'domtel', 'mobtel', 'importance', 'claim_type', 'line_type', )}),
        ('vukonanya', {'fields': (('planning_date_from', 'planning_time_from', 'planning_time_to', 'status', 'disclaimer'), 'who_do', 'what_do')}),
        ('comments', {'fields': ['comments']}),
        ('advanced', {'classes': ('collapse',), 'fields': ['claims_group']}),
    ]
    list_display = ('pk_num', 'importance_vyl', 'importance_kv', 'login_mod', 'importance_error', 'importance_who_give', 'format_pub_date', 'who_do', 'same_claim_view', 'line_type','info', 'planning',)
    list_display_links = ('importance_vyl',)

    def planning(self, obj):

        if not obj.status:

            # blink full date

            if obj.planning_date_from and obj.planning_time_from and obj.planning_time_to:
                date_from = obj.planning_date_from.strftime('%d')
                time_from = obj.planning_time_from.strftime('%H:%M')
                time_to = obj.planning_time_to.strftime('%H:%M')
                return '''<span class="blink_%s">На %s з %s до %s</span><script>
                Date.prototype.timeNow = function () {
                    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes();
                };
                var currentTime = new Date();
                var day = currentTime.getDate();
                var day_from_%s = "%s";
                var time_from_%s = "%s";
                var time_to_%s = "%s";
                var my_time = currentTime.timeNow();

                function blink(e) {
                    $(e).fadeOut(1500, function () {
                        $(this).fadeIn(500, function () {
                            blink(this);
                        });
                    });
                }

                function check_blink_%s() {
                    if (day >= day_from_%s & my_time >= time_from_%s & my_time <= time_to_%s) {
                        blink(".blink_%s");
                    }
                }

                setInterval('check_blink_%s()', 1000);

                </script>''' % (obj.pk, date_from, time_from, time_to, obj.pk, date_from, obj.pk, time_from, obj.pk, time_to, obj.pk, obj.pk, obj.pk, obj.pk, obj.pk, obj.pk, )

            # blink date_from & time_from

            if obj.planning_date_from and obj.planning_time_from:
                date_from = obj.planning_date_from.strftime('%d')
                time_from = obj.planning_time_from.strftime('%H:%M')
                return '''<span class="blink_%s">На %s з %s</span><script>
                Date.prototype.timeNow = function () {
                    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes();
                };
                var currentTime = new Date();
                var day = currentTime.getDate();
                var day_from_%s = "%s";
                var time_from_%s = "%s";
                var my_time = currentTime.timeNow();

                function blink(e) {
                    $(e).fadeOut(1500, function () {
                        $(this).fadeIn(500, function () {
                            blink(this);
                        });
                    });
                }

                function check_blink_%s() {
                    if (day >= day_from_%s & my_time >= time_from_%s) {
                        blink(".blink_%s");
                    }
                }

                setInterval('check_blink_%s()', 1000);

                </script>''' % (obj.pk, date_from, time_from, obj.pk, date_from, obj.pk, time_from, obj.pk, obj.pk, obj.pk, obj.pk, obj.pk, )
            if obj.planning_date_from and obj.planning_time_to:
                date_from = obj.planning_date_from.strftime('%d')
                time_to = obj.planning_time_to.strftime('%H:%M')
                return '''<span class="blink_%s">На %s до %s</span><script>
                Date.prototype.timeNow = function () {
                    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes();
                };
                var currentTime = new Date();
                var day = currentTime.getDate();
                var day_from_%s = "%s";
                var time_to_%s = "%s";
                var my_time = currentTime.timeNow();

                function blink(e) {
                    $(e).fadeOut(1500, function () {
                        $(this).fadeIn(500, function () {
                            blink(this);
                        });
                    });
                }

                function check_blink_%s() {
                    if (day >= day_from_%s & my_time <= time_to_%s) {
                        blink(".blink_%s");
                    }
                }

                setInterval('check_blink_%s()', 1000);

                </script>''' % (obj.pk, date_from, time_to, obj.pk, date_from, obj.pk, time_to, obj.pk, obj.pk, obj.pk, obj.pk, obj.pk, )
            if obj.planning_date_from:
                date_from = obj.planning_date_from.strftime('%d')
                return '''<span class="blink_%s">На %s</span><script>
                Date.prototype.timeNow = function () {
                    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes();
                };
                var currentTime = new Date();
                var day = currentTime.getDate();
                var day_from_%s = "%s";
                var my_time = currentTime.timeNow();

                function blink(e) {
                    $(e).fadeOut(1500, function () {
                        $(this).fadeIn(500, function () {
                            blink(this);
                        });
                    });
                }

                function check_blink_%s() {
                    if (day >= day_from_%s) {
                        blink(".blink_%s");
                    }
                }

                setInterval('check_blink_%s()', 1000);

                </script>''' % (obj.pk, date_from, obj.pk, date_from, obj.pk, obj.pk, obj.pk, obj.pk, )
            if obj.planning_time_from and obj.planning_time_to:
                time_from = obj.planning_time_from.strftime('%H:%M')
                time_to = obj.planning_time_to.strftime('%H:%M')
                return '''<span class="blink_%s">З %s до %s</span><script>
                Date.prototype.timeNow = function () {
                    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes();
                };
                var currentTime = new Date();
                var time_from_%s = "%s";
                var time_to_%s = "%s";
                var my_time = currentTime.timeNow();

                function blink(e) {
                    $(e).fadeOut(1500, function () {
                        $(this).fadeIn(500, function () {
                            blink(this);
                        });
                    });
                }

                function check_blink_%s() {
                    if (my_time >= time_from_%s & my_time <= time_to_%s) {
                        blink(".blink_%s");
                    }
                }

                setInterval('check_blink_%s()', 1000);

                </script>''' % (obj.pk, time_from, time_to, obj.pk, time_from, obj.pk, time_to, obj.pk, obj.pk, obj.pk, obj.pk, obj.pk, )
            if obj.planning_time_from:
                time_from = obj.planning_time_from.strftime('%H:%M')
                return '''<span class="blink_%s">З %s</span><script>
                Date.prototype.timeNow = function () {
                    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes();
                };
                var currentTime = new Date();
                var time_from_%s = "%s";
                var my_time = currentTime.timeNow();

                function blink(e) {
                    $(e).fadeOut(1500, function () {
                        $(this).fadeIn(500, function () {
                            blink(this);
                        });
                    });
                }

                function check_blink_%s() {
                    if (my_time >= time_from_%s) {
                        blink(".blink_%s");
                    }
                }

                setInterval('check_blink_%s()', 1000);

                </script>''' % (obj.pk, time_from, obj.pk, time_from, obj.pk, obj.pk, obj.pk, obj.pk, )
            if obj.planning_time_to:
                time_to = obj.planning_time_to.strftime('%H:%M')
                return '''<span class="blink_%s">До %s</span><script>
                Date.prototype.timeNow = function () {
                    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes();
                };
                var currentTime = new Date();
                var time_to_%s = "%s";
                var my_time = currentTime.timeNow();

                function blink(e) {
                    $(e).fadeOut(1500, function () {
                        $(this).fadeIn(500, function () {
                            blink(this);
                        });
                    });
                }

                function check_blink_%s() {
                    if (my_time <= time_to_%s) {
                        blink(".blink_%s");
                    }
                }

                setInterval('check_blink_%s()', 1000);

                </script>''' % (obj.pk, time_to, obj.pk, time_to, obj.pk, obj.pk, obj.pk, obj.pk, )
            else:
                return ''
        else:
            # blink full date
            if obj.planning_date_from and obj.planning_time_from and obj.planning_time_to:
                date_from = obj.planning_date_from.strftime('%d')
                time_from = obj.planning_time_from.strftime('%H:%M')
                time_to = obj.planning_time_to.strftime('%H:%M')
                print date_from, time_from, time_to
                return '<span class="blink">На %s з %s до %s</span>' % (date_from, time_from, time_to,)

            # blink date_from & time_from

            if obj.planning_date_from and obj.planning_time_from:
                date_from = obj.planning_date_from.strftime('%d')
                time_from = obj.planning_time_from.strftime('%H:%M')
                print date_from, time_from
                return '''<span class="blink">На %s з %s</span>''' % (date_from, time_from,)
            if obj.planning_date_from and obj.planning_time_to:
                date_from = obj.planning_date_from.strftime('%d')
                time_to = obj.planning_time_to.strftime('%H:%M')
                return '<span class="blink">На %s до %s</span>' % (date_from, time_to,)
            if obj.planning_date_from:
                date_from = obj.planning_date_from.strftime('%d')
                return '<span class="blink">На %s</span>' % (date_from,)
            if obj.planning_time_from and obj.planning_time_to:
                time_from = obj.planning_time_from.strftime('%H:%M')
                time_to = obj.planning_time_to.strftime('%H:%M')
                return '<span class="blink">З %s до %s</span>' % (time_from, time_to)
            if obj.planning_time_from:
                time_from = obj.planning_time_from.strftime('%H:%M')
                return '<span class="blink">З %s</span>' % (time_from,)
            if obj.planning_time_to:
                time_to = obj.planning_time_to.strftime('%H:%M')
                return '<span class="blink">До %s</span>' % (time_to,)
            else:
                return ''

    planning.allow_tags = True
    planning.short_description = 'Планування'


    def pk_num(self, ClaimInternet):
        return ('<span>%s</span>' % (ClaimInternet.pk))
    pk_num.allow_tags = True
    pk_num.short_description = '№'
    pk_num.admin_order_field = 'pk'


    def info(self, ClaimInternet):
        domtel = u'Дом тел'
        mobtel = u'Моб тел'
        group = u'Група'
        comments = u'Коменти'
        return '''<a id="info_%s" class="btn btn-success" href="#" data-original-title="" title=""></a>
                    <ul class="dropdown-menu" id="help_text_content_%s">
                        <li class="list-group-item">%s - %s</li>
                        <li class="list-group-item">%s - %s</li>
                        <li class="list-group-item">%s - %s</li>
                        <li class="list-group-item">%s - %s</li>
                    </ul>
                    <script>
                        $(function (){$('#info_%s').popover({
                            placement: 'bottom',
                            html : true,
                            content: function() {return $('#help_text_content_%s').html();
                            }});
                        });

                        $('body').on('click', function (e) {
                            $('#info_%s').each(function () {
                                //the 'is' for buttons that triggers popups
                                //the 'has' for icons within a button that triggers a popup
                                if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('#info_%s').has(e.target).length === 0) {
                                    $(this).popover('hide');
                                }
                            });
                        });
                    </script>''' % (ClaimInternet.pk, ClaimInternet.pk, domtel, ClaimInternet.domtel, mobtel, ClaimInternet.mobtel, group, ClaimInternet.claims_group, comments, ClaimInternet.comments, ClaimInternet.pk, ClaimInternet.pk,ClaimInternet.pk, ClaimInternet.pk,  )
    info.allow_tags = True
    info.short_description = 'Інфо'

    def same_claim_view(self, ClaimInternet):
        if ClaimInternet.same_claim >= 1:
            return ('<div align="center" id="same_zayavka" style="background-color: red"><span style="color: white">%s</span></div>' % (ClaimInternet.same_claim))
        else:
            return ('<div align="center">%s</div>' % (ClaimInternet.same_claim))

    same_claim_view.allow_tags = True
    same_claim_view.short_description = 'Повтори'
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
            return '<span id="%s" title="|| %s || %s || %s">%s</span>' % (ClaimInternet.pk, ClaimInternet.domtel, ClaimInternet.mobtel, ClaimInternet.comments.replace('"','&quot;').replace("'","&apos;"), ClaimInternet.vyl)
        if ClaimInternet.importance_id == 2:
            return '<span id="%s" style="color: #008000;" title="|| %s || %s || %s">%s</span>' % (ClaimInternet.pk, ClaimInternet.domtel, ClaimInternet.mobtel, ClaimInternet.comments.replace('"','&quot;').replace("'","&apos;"), ClaimInternet.vyl)
        if ClaimInternet.importance_id == 3:
            return '<span id="%s" style="color: #dc0000;" title="|| %s || %s || %s">%s</span>' % (ClaimInternet.pk, ClaimInternet.domtel, ClaimInternet.mobtel, ClaimInternet.comments.replace('"','&quot;').replace("'","&apos;"), ClaimInternet.vyl)
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

    def login_mod(self, ClaimInternet):
        return '''<a id="id_login_%s" class="" rel="" href="#" data-original-title="" title="">%s</a>
                    <ul class="dropdown-menu" id="help_text_content_%s">
                        <li class="list-group-item">
                            <a href="https://192.168.33.80:9443/admin/index.cgi?index=7&search=1&type=11&LOGIN_EXPR=%s" target="_blank">Bill</a>
                        </li>
                        <li class="list-group-item">
                            <a href="http://192.168.33.41:8888/admin/abon/user/?q=%s" target="_blank">ARP</a>
                        </li>
                    </ul>
                    <script>
                        $(function (){
                            $('#id_login_%s').popover({
                                placement: 'bottom',
                                html : true,
                                content: function() {return $('#help_text_content_%s').html();
                            }});
                        });
                        $('body').on('click', function (e) {
                            $('#id_login_%s').each(function () {
                                //the 'is' for buttons that triggers popups
                                //the 'has' for icons within a button that triggers a popup
                                if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('#id_login_%s').has(e.target).length === 0) {
                                    $(this).popover('hide');
                                }
                            });
                        });
                    </script>''' % (ClaimInternet.login, ClaimInternet.login, ClaimInternet.login, ClaimInternet.login, ClaimInternet.login, ClaimInternet.login, ClaimInternet.login, ClaimInternet.login, ClaimInternet.login)
    login_mod.allow_tags = True
    login_mod.short_description = 'Логін'
    login_mod.admin_order_field = 'login'

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
                   'disclaimer',
                   ('who_do', ClaimsInternetFilter),
                   'importance',
                   'claims_group',
                   ('pub_date', DateRangeFilter)]

    search_fields = ['id', 'vyl__sorting', 'kv', 'login', 'error__name', 'who_give', 'domtel', 'mobtel', 'who_do__name', 'what_do', 'importance__status_importance']
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


from django.contrib.auth.decorators import login_required
class ClaimCtvAdmin(admin.ModelAdmin):

    def claims_print(self, request):
        from .form import PrintFilterForm
        if request.method == 'GET':
            request.session['status'] = request.GET.get('status', 0)
            status = request.session.get('status', request.session.get('status', 0))
            request.session['worker'] = request.GET.get('worker', None)
            worker = request.session.get('worker', request.session['worker'])
        claims = ClaimCtv.objects.filter(status=False)
        if not status == 'None':
            claims = claims.filter(Q(status=status))
        if worker:
            claims = claims.filter(Q(who_do__id=worker))
        print_form = PrintFilterForm(initial={'status': status, 'worker': worker})
        return render_to_response('admin/claim-ctv/print.html', {
                        'worker': request.session['worker'],
                        'status': request.session['status'],
                        'claims': claims,
                        'print_form': print_form,
                    }, context_instance=RequestContext(request))

    class Media:
        css = {
            "all": ("/static/css/ui-lightness/jquery-ui-1.10.3.custom.min.css", "/static/css/custom.css")
        }
        js = (
            "/static/js/filter.js",
            "/static/js/button.js",
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
        try:
            test = request.META['HTTP_REFERER'].split(request.META['PATH_INFO'])
            if test and test[-1] and not test[-1].startswith('?') and not request.GET.has_key('status__exact') and not request.GET.has_key('disclaimer__exact'):
                return HttpResponseRedirect("/admin/claim/claimctv/?disclaimer__exact=0&status__exact=0")
        except:
            pass # In case there is no referer
        return super(ClaimCtvAdmin,self).changelist_view(request, extra_context=extra_context)

    fieldsets = [
        ('zayavka:', {'fields': ('vyl', 'kv', 'error', 'domtel', 'mobtel', 'importance', 'group', )}),
        ('vukonanya', {'fields': ('status', 'disclaimer', 'who_do', 'what_do')}),
        ('comments', {'fields': ['comments']}),
    ]
    list_display = ('importance_vyl', 'importance_kv', 'importance_error', 'domtel', 'mobtel', 'importance_who_give', 'pub_date', 'who_do','same_claim_view', 'group',)


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
    list_filter = ['status', 'disclaimer', ('who_do', ClaimsCtvFilter), 'group', ('pub_date', DateRangeFilter)]
    search_fields = ['vyl__sorting', 'kv', 'error__name',]
    save_on_top = True
    filter_horizontal = ('what_do',)
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
#admin.site.register(PrinterAdmin)
admin.site.register(Importance)
admin.site.register(Vyl)
admin.site.register(House)
admin.site.register(Error)
admin.site.register(Error_type)
admin.site.register(Line_type)
