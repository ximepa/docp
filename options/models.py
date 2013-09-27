# -*- coding: utf-8 -*-
from django.db import models


class Dom(models.Model):
    vyl = models.ForeignKey('Vyl', verbose_name='Вулиця')
    house = models.ForeignKey('House', verbose_name='Будинок')
    sorting = models.CharField(max_length=200, blank=True, unique=True)

    def __unicode__(self):
        return self.sorting

    def save(self):
        self.sorting = "%s %s" % (self.vyl.name, self.house.num)
        super(Dom, self).save()

    class Meta:
        ordering = ('sorting',)
        verbose_name = u'дом'
        verbose_name_plural = u'дома'
        unique_together = ('vyl', 'house')


class Vyl(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Назва вулиці', )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Вулиця'
        verbose_name_plural = u'Вулиці'


class House(models.Model):
    num = models.CharField(max_length=200, unique=True, verbose_name='№ будинку', )

    def __unicode__(self):
        return self.num

    class Meta:
        ordering = ('num',)
        verbose_name = u'№ Будиноку'
        verbose_name_plural = u'№ Будинку'


class Worker(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Жалобщик', )
    is_active = models.BooleanField(default=False)
    work_type = models.ForeignKey('Work_type', verbose_name='Тип поботи')
    notebook_ip = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Жалобщик'
        verbose_name_plural = u'Жалобщики'


class Work_type(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Тип роботи')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Тип роботи'
        verbose_name_plural = u'Тип роботи'


class Importance(models.Model):
    status_importance = models.CharField(max_length=200, unique=True, verbose_name='Важливість')

    def __unicode__(self):
        return self.status_importance

    class Meta:
        ordering = ('status_importance',)
        verbose_name = u'Важливість'
        verbose_name_plural = u'Важливість'


class Error(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Помилка')
    type = models.ForeignKey('Error_type', verbose_name='Тип')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Помилка'
        verbose_name_plural = u'Помилки'


class Error_type(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Тип помилки')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Тип помилки'
        verbose_name_plural = u'Типи помилок'


class Line_type(models.Model):
    name = models.CharField(max_length=200,  verbose_name='Тип помилки', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Тип лінії'
        verbose_name_plural = u'Типи ліній'


class Claim_type(models.Model):
    name = models.CharField(max_length=200,  verbose_name='Тип заявки', unique=True)
    type = models.ForeignKey(Work_type, verbose_name='Тип')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Тип заявки'
        verbose_name_plural = u'Типи заявок'


class Claims_group(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True,  verbose_name='Інтернет бригади')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Інтернет бригади'
        verbose_name_plural = u'Інтернет бригади'


# Ctv
class PerformedWork(models.Model):
    name = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'КТБ виконана робота'
        verbose_name_plural = 'КТБ виконані роботи'


class Group(models.Model):
    group_name = models.CharField(max_length=200, blank=True, null=True,  verbose_name='КТБ групи')

    def __unicode__(self):
        return self.group_name

    class Meta:
        ordering = ('group_name',)
        verbose_name = 'КТБ група'
        verbose_name_plural = 'КТБ групи'