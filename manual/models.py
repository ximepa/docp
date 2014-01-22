# -*- coding: utf-8 -*- 
from django.db import models

class Manual(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=30, blank=True)
    description = models.TextField()
    #image = models.ImageField(upload_to='uploads')
    lock = models.BooleanField(default=False)
    group = models.ForeignKey('Manualgroup')
    author = models.CharField(max_length = 100, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    url = models.URLField(auto_created=True, blank=True)

    def __unicode__(self):
        return self.name

class Manualgroup(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
