from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext


def index(request):
    text = 'hello world'
    return render(request, 'planning/index.html', {
        'text': text,
    })
