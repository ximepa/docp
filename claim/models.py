# -*- coding: utf-8 -*-
from django.db import models
from options.models import *
from lib import TimedeltaField

# Інтернет заявки
class ClaimInternet(models.Model):
    vyl = models.ForeignKey(Dom, verbose_name='Вулиця')
    kv = models.CharField(max_length=200, verbose_name='Кв.', blank=True)
    login = models.CharField(max_length=200, verbose_name='Логін')
    error = models.ForeignKey(Error, verbose_name='Помилка')
    who_give = models.CharField(max_length=200, editable=False, verbose_name='Додав')
    who_do = models.ForeignKey(Worker, blank=True, null=True, verbose_name='Виконавець')
    what_do = models.CharField(max_length=200, blank=True, null=True, verbose_name='Виконані роботи')
    datetime = models.DateTimeField(verbose_name='Дата вик', auto_now_add = True)
    date_give = models.DateTimeField(verbose_name='Отримав', auto_now_add = True)
    date_change = TimedeltaField(verbose_name='Різниця', blank=True, null=True, )
    status = models.BooleanField(default=False, verbose_name='Виконана')
    disclaimer = models.BooleanField(default=False, verbose_name='Відмова')
    importance = models.ForeignKey(Importance, verbose_name='Важливість', default=1)
    pub_date = models.DateTimeField(verbose_name='Дата створення', auto_now_add = True, editable=False, blank=True)
    comments = models.TextField(max_length=200, blank=True, null=True,  verbose_name='Коментарії')
    domtel = models.CharField(max_length=200, blank=True, null=True,  verbose_name='Домашній т.')
    mobtel = models.CharField(max_length=200, blank=True, null=True,  verbose_name='Мобільний т.')
    planning_date_from = models.DateField(verbose_name='Date from', blank=True)
    planning_time_from = models.TimeField(verbose_name='Time from', blank=True)
    planning_time_to = models.TimeField(verbose_name='Time to', blank=True)
    claim_type = models.ForeignKey(Claim_type, verbose_name='Тип заявки', default=1)
    line_type = models.ForeignKey(Line_type, verbose_name='Тип лінії', default=1)
    same_claim = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Схожі заявки')
    claims_group = models.ForeignKey(Claims_group, verbose_name='Група заявки', default=1)

    def __unicode__(self):
        return self.vyl.sorting

    def get_json(self):
        return {
            'id': self.pk,
            'vyl': self.vyl,
            'error': self.error
        }

    def claim_internet_count(self):
        claim_inet_count = ClaimInternet.objects.all().count()
        return claim_inet_count

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = u'Інтернет заявки'
        verbose_name_plural = u'Інтернет заявки'

    def save(self,*args, **kwargs):
        from datetime import datetime, timedelta
        try:
            obj = self.__class__.objects.get(pk=self.pk)
        except:
            obj = None
        if (not obj or not obj.status) and self.status:
            self.datetime = datetime.now()
            self.date_change = (self.datetime - self.date_give)
        if (not obj or not obj.who_do) and self.who_do:
            self.date_give = datetime.now()
        super(ClaimInternet, self).save(*args, **kwargs)
        self.same_claim = self.__class__.objects.filter(login=self.login).filter(pub_date__gte=(datetime.today()-timedelta(180) )).count()-1
        super(ClaimInternet, self).save(*args, **kwargs)


# Кабельні заявки
class ClaimCtv(models.Model):
    vyl = models.ForeignKey(Dom, verbose_name='Вулиця')
    kv = models.CharField(max_length=200, verbose_name='Кв.', blank=True)
    error = models.ForeignKey(Error, verbose_name='Помилка')
    who_do = models.ForeignKey(Worker, blank=True, null=True, verbose_name='Виконавець')
    who_give = models.CharField(max_length=200, editable=False, verbose_name='Додав')
    what_do = models.ManyToManyField(PerformedWork, blank=True, null=True, verbose_name=u'Виконані роботи')
    datetime = models.DateTimeField(verbose_name='Дата вик', auto_now_add = True)
    date_give = models.DateTimeField(verbose_name='Отримав', auto_now_add = True)
    date_change = TimedeltaField(verbose_name='Різниця', blank=True, null=True, )
    status = models.BooleanField(default=False, verbose_name='Виконана')
    disclaimer = models.BooleanField(default=False, verbose_name='Відмова')
    importance = models.ForeignKey(Importance, verbose_name='Важливість', default=1)
    pub_date = models.DateTimeField(verbose_name='Дата створення', auto_now_add = True, editable=False, blank=True)
    comments = models.TextField(max_length=200, blank=True, null=True,  verbose_name='Коментарії')
    domtel = models.CharField(max_length=200, blank=True, null=True,  verbose_name='Домашній т.', help_text='Если много номеров указывать через кому')
    mobtel = models.CharField(max_length=200, blank=True, null=True,  verbose_name='Мобільний т.', help_text='Если много номеров указывать через кому')
    same_claim = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Схожі заявки')
    group = models.ForeignKey(Group, verbose_name='Группа', default=1)

    def __unicode__(self):
        return self.vyl.sorting

    def claim_ctb_count(self):
        claim_count = ClaimInternet.objects.all().count()
        return claim_count

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'КТБ заявки'
        verbose_name_plural = 'КТБ заявки'

    def save(self,*args, **kwargs):
        from datetime import datetime, timedelta
        try:
            obj = self.__class__.objects.get(pk=self.pk)
        except:
            obj = None
        if (not obj or not obj.status) and self.status:
            self.datetime = datetime.now()
            self.date_change = (self.datetime - self.date_give)
        if (not obj or not obj.who_do) and self.who_do:
            self.date_give = datetime.now()
        super(ClaimCtv, self).save(*args, **kwargs)
        self.same_claim = self.__class__.objects.filter(vyl=self.vyl, kv=self.kv).filter(pub_date__gte=(datetime.today()-timedelta(180) )).count()-1
        super(ClaimCtv, self).save(*args, **kwargs)