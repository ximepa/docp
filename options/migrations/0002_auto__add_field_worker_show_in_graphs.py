# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Worker.show_in_graphs'
        db.add_column(u'options_worker', 'show_in_graphs',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Worker.show_in_graphs'
        db.delete_column(u'options_worker', 'show_in_graphs')


    models = {
        u'options.claim_type': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Claim_type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'options.claims_group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Claims_group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'options.dom': {
            'Meta': {'ordering': "('sorting',)", 'unique_together': "(('vyl', 'house'),)", 'object_name': 'Dom'},
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.House']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sorting': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'vyl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Vyl']"})
        },
        u'options.error': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Error'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Error_type']"})
        },
        u'options.error_type': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Error_type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'options.group': {
            'Meta': {'ordering': "('group_name',)", 'object_name': 'Group'},
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'options.house': {
            'Meta': {'ordering': "('num',)", 'object_name': 'House'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'options.importance': {
            'Meta': {'ordering': "('status_importance',)", 'object_name': 'Importance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_importance': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'options.line_type': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Line_type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'options.performedwork': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PerformedWork'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        u'options.vyl': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Vyl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'options.work_type': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Work_type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'options.worker': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Worker'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'notebook_ip': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'show_in_graphs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Work_type']"})
        }
    }

    complete_apps = ['options']