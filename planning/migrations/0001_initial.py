# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PlanningConnections'
        db.create_table(u'planning_planningconnections', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vyl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Dom'])),
            ('kv', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'planning', ['PlanningConnections'])


    def backwards(self, orm):
        # Deleting model 'PlanningConnections'
        db.delete_table(u'planning_planningconnections')


    models = {
        u'options.dom': {
            'Meta': {'ordering': "('sorting',)", 'unique_together': "(('vyl', 'house'),)", 'object_name': 'Dom'},
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.House']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sorting': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'vyl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Vyl']"})
        },
        u'options.house': {
            'Meta': {'ordering': "('num',)", 'object_name': 'House'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'options.vyl': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Vyl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'planning.planningconnections': {
            'Meta': {'object_name': 'PlanningConnections'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kv': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'vyl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Dom']"})
        }
    }

    complete_apps = ['planning']