# -*- encoding: utf-8 -*-
__author__ = 'maxim'

# -*- encoding: utf-8 -*-
from djangorpc import Error, Msg, RpcHttpResponse
from .models import PlanningConnections
from.forms import PlanningConnectionsForm
from tim.decorators import get_json
from djangorpc.decorators import form_handler
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from datetime import datetime

class CalendarApiClass(object):

    def hello(self, user):
        return Msg("Hello")

    @get_json
    def events_get(self, start, end, user):
        return PlanningConnections.objects.filter(start__gte=start, end__lte=end)

    @form_handler
    def events_set(self, rdata, user):
        if 'instance_id' in rdata and rdata['instance_id']:
            event_id = rdata.pop('instance_id')[0]
            try:
                event = PlanningConnections.objects.get(pk=event_id)
            except PlanningConnections.DoesNotExist:
                return Error(_("Update error. Entry not found"))
            else:
                if 'action_delete' in rdata and rdata['action_delete']:
                    event.delete()
                    response = RpcHttpResponse()
                    response['success'] = True
                    response['msg'] = "deleted"
                    return response
                print rdata
                print event
                dt = {
                    'start': rdata.get('start',None),
                    'end': rdata.get('end',None)
                }
                print dt
                form = PlanningConnectionsForm(dt
                , instance=event)
        else:
            form = PlanningConnectionsForm(dict(rdata))
        if form.is_valid():
            form.save()
            response = RpcHttpResponse()
            response['success'] = True
            response['msg'] = "saved"
            return response
        else:
            print form.errors
            print form.cleaned_data
            return Error(form.errors)
