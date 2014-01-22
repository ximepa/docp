# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dom'
        db.create_table(u'options_dom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vyl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Vyl'])),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.House'])),
            ('sorting', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, blank=True)),
        ))
        db.send_create_signal(u'options', ['Dom'])

        # Adding unique constraint on 'Dom', fields ['vyl', 'house']
        db.create_unique(u'options_dom', ['vyl_id', 'house_id'])

        # Adding model 'Vyl'
        db.create_table(u'options_vyl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'options', ['Vyl'])

        # Adding model 'House'
        db.create_table(u'options_house', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'options', ['House'])

        # Adding model 'Worker'
        db.create_table(u'options_worker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Work_type'])),
            ('notebook_ip', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'options', ['Worker'])

        # Adding model 'Work_type'
        db.create_table(u'options_work_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'options', ['Work_type'])

        # Adding model 'Importance'
        db.create_table(u'options_importance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status_importance', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'options', ['Importance'])

        # Adding model 'Error'
        db.create_table(u'options_error', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Error_type'])),
        ))
        db.send_create_signal(u'options', ['Error'])

        # Adding model 'Error_type'
        db.create_table(u'options_error_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'options', ['Error_type'])

        # Adding model 'Line_type'
        db.create_table(u'options_line_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'options', ['Line_type'])

        # Adding model 'Claim_type'
        db.create_table(u'options_claim_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'options', ['Claim_type'])

        # Adding model 'Claims_group'
        db.create_table(u'options_claims_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'options', ['Claims_group'])

        # Adding model 'PerformedWork'
        db.create_table(u'options_performedwork', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal(u'options', ['PerformedWork'])

        # Adding model 'Group'
        db.create_table(u'options_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'options', ['Group'])


    def backwards(self, orm):
        # Removing unique constraint on 'Dom', fields ['vyl', 'house']
        db.delete_unique(u'options_dom', ['vyl_id', 'house_id'])

        # Deleting model 'Dom'
        db.delete_table(u'options_dom')

        # Deleting model 'Vyl'
        db.delete_table(u'options_vyl')

        # Deleting model 'House'
        db.delete_table(u'options_house')

        # Deleting model 'Worker'
        db.delete_table(u'options_worker')

        # Deleting model 'Work_type'
        db.delete_table(u'options_work_type')

        # Deleting model 'Importance'
        db.delete_table(u'options_importance')

        # Deleting model 'Error'
        db.delete_table(u'options_error')

        # Deleting model 'Error_type'
        db.delete_table(u'options_error_type')

        # Deleting model 'Line_type'
        db.delete_table(u'options_line_type')

        # Deleting model 'Claim_type'
        db.delete_table(u'options_claim_type')

        # Deleting model 'Claims_group'
        db.delete_table(u'options_claims_group')

        # Deleting model 'PerformedWork'
        db.delete_table(u'options_performedwork')

        # Deleting model 'Group'
        db.delete_table(u'options_group')


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
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Work_type']"})
        }
    }

    complete_apps = ['options']