from django import forms
from django.contrib.auth.forms import AuthenticationForm
from manual.models import *



class ManualFilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'},))