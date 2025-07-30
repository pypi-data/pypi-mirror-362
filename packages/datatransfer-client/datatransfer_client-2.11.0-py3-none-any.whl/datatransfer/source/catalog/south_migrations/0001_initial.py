# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FeedBack'
        db.create_table('catalog_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('result', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('xml', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('archive', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('last_update_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('catalog', ['FeedBack'])

        # Adding model 'FeedBackStatistic'
        db.create_table('catalog_feedbackstatistic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.FeedBack'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('model_verbose', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
            ('invalid', self.gf('django.db.models.fields.IntegerField')()),
            ('processed', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.IntegerField')()),
            ('updated', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('catalog', ['FeedBackStatistic'])

        # Adding model 'FeedBackDetails'
        db.create_table('catalog_feedbackdetails', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback_statistic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.FeedBackStatistic'])),
            ('record_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('catalog', ['FeedBackDetails'])


    def backwards(self, orm):
        # Deleting model 'FeedBack'
        db.delete_table('catalog_feedback')

        # Deleting model 'FeedBackStatistic'
        db.delete_table('catalog_feedbackstatistic')

        # Deleting model 'FeedBackDetails'
        db.delete_table('catalog_feedbackdetails')


    models = {
        'catalog.feedback': {
            'Meta': {'object_name': 'FeedBack'},
            'archive': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update_date': ('django.db.models.fields.DateField', [], {}),
            'result': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'xml': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'catalog.feedbackdetails': {
            'Meta': {'object_name': 'FeedBackDetails'},
            'feedback_statistic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.FeedBackStatistic']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'record_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'catalog.feedbackstatistic': {
            'Meta': {'object_name': 'FeedBackStatistic'},
            'created': ('django.db.models.fields.IntegerField', [], {}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.FeedBack']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invalid': ('django.db.models.fields.IntegerField', [], {}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'model_verbose': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'processed': ('django.db.models.fields.IntegerField', [], {}),
            'total': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['catalog']