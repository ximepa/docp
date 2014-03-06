# -*- coding: utf-8 -*-
__author__ = 'ximepa'
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from claim.models import *


class ChangeInternetWorkerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    worker = forms.ModelChoiceField(queryset=Worker.objects.all().filter(is_active=True, work_type__name__icontains='Інтернет'), label=u'Працівник', required=False)

class ChangeCtvWorkerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    worker = forms.ModelChoiceField(queryset=Worker.objects.all().filter(is_active=True, work_type__name__icontains='Кабельне'), label=u'Працівник', required=False)

class ChangeStatusForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    status = forms.BooleanField(label=u'Статус', required=False)
    disclaimer = forms.BooleanField(label=u'Відмова', required=False)
    what_do = forms.CharField(max_length=200, label=u'Виконані роботи', required=False, widget=forms.Textarea(attrs={'size':'50'}))


class ChangeImportanceForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    importance = forms.ModelChoiceField(queryset=Importance.objects.all(), label=u'Важливість', empty_label=None, initial=1, widget=forms.RadioSelect())

class ClaimAuthenticationForm(AuthenticationForm):
    # add your form widget here
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class ChangeClaims_groupForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    claims_group = forms.BooleanField(label=u'Група заявки', required=False, initial=1)

STATUS_FILTER_CHOISES = (
    (None, 'all'),
    (0, 'Ні'),
    (1, 'Так'),
)


class InternetFilterForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS_FILTER_CHOISES, initial='0', widget=forms.RadioSelect(attrs={'onclick': 'document.getElementById("filter_form").submit();'}),)
    worker = forms.ModelChoiceField(queryset=Worker.objects.all().filter(is_active=True, work_type__id=1),
                                            widget=forms.RadioSelect(attrs={'onclick': 'document.getElementById("filter_form").submit();'}))
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Пошук'},))
    #page = forms.HiddenInput()
    def as_url_args(self):
        import urllib
        return urllib.urlencode(self.status)

class PrintFilterForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS_FILTER_CHOISES, initial='0', widget=forms.Select(attrs={'class': 'selectpicker'}),)
    worker = forms.ModelChoiceField(queryset=Worker.objects.all().filter(is_active=True, work_type__name__icontains='Кабельне'),
                                            widget=forms.Select(attrs={'class': 'selectpicker show-tick',}))




