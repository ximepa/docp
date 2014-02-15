# -*- coding: utf-8 -*-
from django.db import models
from datetime import timedelta
from django.utils import timezone
import datetime


class Dom(models.Model):
    vyl = models.ForeignKey('Vyl', verbose_name='Вулиця')
    house = models.ForeignKey('House', verbose_name='Будинок')
    sorting = models.CharField(max_length=200, blank=True, unique=True)

    def __unicode__(self):
        return self.sorting

    def save(self):
        self.sorting = "%s %s" % (self.vyl.name, self.house.num)
        super(Dom, self).save()

    def get_json(self):
        return {
            'id': self.pk,
            'sorting': self.sorting,
        }


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

    def get_json(self):
        return {
            'id': self.pk,
            'name': self.name,
        }


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
    work_type = models.ForeignKey('Work_type', verbose_name='Тип роботи')
    notebook_ip = models.CharField(max_length=200, blank=True)
    show_in_graphs = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def get_stats_inet_year(self):
        from claim.models import ClaimInternet
        today_year = datetime.date.today().year
        year_list = ClaimInternet.objects.filter(datetime__year=today_year).dates('datetime', 'day')
        worker_stat_year = [{
            'year': str(years.year) + '-' + str(years.month) + '-' + str(years.day),
            'claims_all_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, who_do_id=self.pk).count(),
            'claims_completed_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, status=True, who_do_id=self.pk).count(),
            'claims_disclaim_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, disclaimer=True, who_do_id=self.pk).count(),
            'claims_uncompleted_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, disclaimer=False, status=False, who_do_id=self.pk).count(),
            'claims_given_to_plumber_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, disclaimer=False, status=False, who_do_id=self.pk).count(),
            'id': int(self.pk)
         } for years in year_list]
        return worker_stat_year

    def get_stats_inet_month(self):
        from claim.models import ClaimInternet
        today_year = datetime.date.today().year
        today_month = datetime.date.today().month
        year_list = ClaimInternet.objects.filter(datetime__year=today_year, datetime__month=today_month).dates('datetime', 'day')
        worker_stat_month = [{
            'year': str(years.year) + '-' + str(years.month) + '-' + str(years.day),
            'claims_all_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, who_do_id=self.pk).count(),
            'claims_completed_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, status=True, who_do_id=self.pk).count(),
            'claims_disclaim_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, disclaimer=True, who_do_id=self.pk).count(),
            'claims_uncompleted_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, disclaimer=False, status=False, who_do_id=self.pk, claims_group=1).count(),
            'claims_given_to_plumber_count': ClaimInternet.objects.filter(datetime__year=years.year, datetime__month=years.month, datetime__day=years.day, disclaimer=False, status=False, who_do_id=self.pk, claims_group=2).count(),
            'id': int(self.pk)
         } for years in year_list]
        return worker_stat_month

    def get_stats_inet_week(self):
        from claim.models import ClaimInternet
        day_last_week = timezone.now().date() - timedelta(days=7)
        day_this_week = day_last_week + timedelta(days=8)
        week_list = ClaimInternet.objects.filter(datetime__gte=day_last_week, datetime__lte=day_this_week).dates('datetime', 'day')
        worker_stat_week = [{
            'week': str(week.year) + '-' + str(week.month) + '-' + str(week.day),
            'claims_all_count': ClaimInternet.objects.filter(pub_date__year=week.year, pub_date__month=week.month, pub_date__day=week.day, who_do_id=self.pk).count(),
            'claims_completed_count': ClaimInternet.objects.filter(pub_date__year=week.year, pub_date__month=week.month, pub_date__day=week.day, status=True, who_do_id=self.pk).count(),
            'claims_disclaim_count': ClaimInternet.objects.filter(pub_date__year=week.year, pub_date__month=week.month, pub_date__day=week.day, disclaimer=True, who_do_id=self.pk).count(),
            'claims_uncompleted_count': ClaimInternet.objects.filter(pub_date__year=week.year, pub_date__month=week.month, pub_date__day=week.day, disclaimer=False, status=False, claims_group=1, who_do_id=self.pk).count(),
            'claims_given_to_plumber_count': ClaimInternet.objects.filter(pub_date__year=week.year, pub_date__month=week.month, pub_date__day=week.day, disclaimer=False, status=False, claims_group=2, who_do_id=self.pk).count(),
            'id': int(self.pk)
         } for week in week_list]
        return worker_stat_week

    def get_stat_inet_all(self):
        from claim.models import ClaimInternet
        completed_all = ClaimInternet.objects.filter(who_do_id=self.pk, status=True).count()
        print completed_all
        return completed_all

    def get_stat_inet_year(self):
        from claim.models import ClaimInternet
        today_year = datetime.date.today().year
        completed_year = ClaimInternet.objects.filter(datetime__year=today_year, who_do_id=self.pk, status=True).count()
        print completed_year
        return completed_year

    def get_stat_inet_month(self):
        from claim.models import ClaimInternet
        today_year = datetime.date.today().year
        today_month = datetime.date.today().month
        completed_month = ClaimInternet.objects.filter(datetime__year=today_year, datetime__month=today_month, who_do_id=self.pk, status=True).count()
        print completed_month
        return completed_month

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

    def get_json(self):
        return {
            'id': self.pk,
            'name': self.name,
        }


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