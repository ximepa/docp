from django.db import models
from options.models import *
# Create your models here.


class PlanningConnections(models.Model):
    vyl = models.ForeignKey(Dom, verbose_name='Вулиця')
    kv = models.CharField(max_length=200, verbose_name='Кв.', blank=True)
    start = models.DateField()
    end = models.DateField()

    def __unicode__(self):
        return self.vyl.sorting
