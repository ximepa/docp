from django import forms

from .models import PlanningConnections

class PlanningConnectionsForm(forms.ModelForm):

    class Meta:
        model = PlanningConnections

    def __init__(self,*args,**kw):
        print "form init"
        print args
        print kw
        super(PlanningConnectionsForm, self).__init__(*args,**kw)
