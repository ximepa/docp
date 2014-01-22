# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClaimInternet'
        db.create_table(u'claim_claiminternet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vyl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Dom'])),
            ('kv', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('error', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Error'])),
            ('who_give', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('who_do', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Worker'], null=True, blank=True)),
            ('what_do', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_give', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_change', self.gf('claim.lib.TimedeltaField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('disclaimer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('importance', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['options.Importance'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=200, null=True, blank=True)),
            ('domtel', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('mobtel', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('planning_date_from', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('planning_time_from', self.gf('django.db.models.fields.TimeField')(blank=True)),
            ('planning_time_to', self.gf('django.db.models.fields.TimeField')(blank=True)),
            ('claim_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['options.Claim_type'])),
            ('line_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['options.Line_type'])),
            ('same_claim', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('claims_group', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['options.Claims_group'])),
        ))
        db.send_create_signal(u'claim', ['ClaimInternet'])

        # Adding model 'ClaimCtv'
        db.create_table(u'claim_claimctv', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vyl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Dom'])),
            ('kv', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('error', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Error'])),
            ('who_do', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['options.Worker'], null=True, blank=True)),
            ('who_give', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_give', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_change', self.gf('claim.lib.TimedeltaField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('disclaimer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('importance', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['options.Importance'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=200, null=True, blank=True)),
            ('domtel', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('mobtel', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('same_claim', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['options.Group'])),
        ))
        db.send_create_signal(u'claim', ['ClaimCtv'])

        # Adding M2M table for field what_do on 'ClaimCtv'
        m2m_table_name = db.shorten_name(u'claim_claimctv_what_do')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('claimctv', models.ForeignKey(orm[u'claim.claimctv'], null=False)),
            ('performedwork', models.ForeignKey(orm[u'options.performedwork'], null=False))
        ))
        db.create_unique(m2m_table_name, ['claimctv_id', 'performedwork_id'])


    def backwards(self, orm):
        # Deleting model 'ClaimInternet'
        db.delete_table(u'claim_claiminternet')

        # Deleting model 'ClaimCtv'
        db.delete_table(u'claim_claimctv')

        # Removing M2M table for field what_do on 'ClaimCtv'
        db.delete_table(db.shorten_name(u'claim_claimctv_what_do'))


    models = {
        u'claim.claimctv': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'ClaimCtv'},
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_change': ('claim.lib.TimedeltaField', [], {'null': 'True', 'blank': 'True'}),
            'date_give': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disclaimer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'domtel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Error']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['options.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['options.Importance']"}),
            'kv': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mobtel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'same_claim': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vyl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Dom']"}),
            'what_do': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['options.PerformedWork']", 'null': 'True', 'blank': 'True'}),
            'who_do': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Worker']", 'null': 'True', 'blank': 'True'}),
            'who_give': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'claim.claiminternet': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'ClaimInternet'},
            'claim_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['options.Claim_type']"}),
            'claims_group': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['options.Claims_group']"}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_change': ('claim.lib.TimedeltaField', [], {'null': 'True', 'blank': 'True'}),
            'date_give': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disclaimer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'domtel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Error']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['options.Importance']"}),
            'kv': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'line_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['options.Line_type']"}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mobtel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'planning_date_from': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'planning_time_from': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'planning_time_to': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'same_claim': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vyl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Dom']"}),
            'what_do': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'who_do': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['options.Worker']", 'null': 'True', 'blank': 'True'}),
            'who_give': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
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

    complete_apps = ['claim']