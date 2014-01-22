from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from .forms import PlanningConnectionsForm

def index(request):
    text = 'hello world'
    return render(request, 'planning/index.html', {
        'text': text,
        'form': PlanningConnectionsForm().as_p
    })
