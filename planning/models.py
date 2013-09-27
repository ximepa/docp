# -*- encoding: utf-8 -*-

from django.db import models
from options.models import *
# Create your models here.


class PlanningConnections(models.Model):
    vyl = models.ForeignKey(Dom, verbose_name=u'Вулиця')
    kv = models.CharField(max_length=200, verbose_name=u'Кв.', blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return self.vyl.sorting

    def get_json(self):

        return {
            'id': self.pk,
            'start': self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': self.end.strftime("%Y-%m-%dT%H:%M:%S"),
            'allDay': False,                             # for fullcalendar
            'title': "%s %s" % (self.vyl.sorting, self.kv)
        }
