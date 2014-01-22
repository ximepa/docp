# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Manual'
        db.create_table(u'manual_manual', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('lock', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manual.Manualgroup'])),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'manual', ['Manual'])

        # Adding model 'Manualgroup'
        db.create_table(u'manual_manualgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'manual', ['Manualgroup'])


    def backwards(self, orm):
        # Deleting model 'Manual'
        db.delete_table(u'manual_manual')

        # Deleting model 'Manualgroup'
        db.delete_table(u'manual_manualgroup')


    models = {
        u'manual.manual': {
            'Meta': {'object_name': 'Manual'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manual.Manualgroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'manual.manualgroup': {
            'Meta': {'object_name': 'Manualgroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['manual']