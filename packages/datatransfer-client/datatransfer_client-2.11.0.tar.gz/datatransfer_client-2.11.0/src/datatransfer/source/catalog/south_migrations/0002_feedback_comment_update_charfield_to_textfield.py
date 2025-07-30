# -*- coding: utf-8 -*-
from __future__ import absolute_import
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'FeedBack.comment'
        db.alter_column(u'catalog_feedback', 'comment', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'FeedBack.comment'
        db.alter_column(u'catalog_feedback', 'comment', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    models = {
        u'catalog.feedback': {
            'Meta': {'object_name': 'FeedBack'},
            'archive': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update_date': ('django.db.models.fields.DateField', [], {}),
            'result': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'xml': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.feedbackdetails': {
            'Meta': {'object_name': 'FeedBackDetails'},
            'feedback_statistic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.FeedBackStatistic']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'record_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'catalog.feedbackstatistic': {
            'Meta': {'object_name': 'FeedBackStatistic'},
            'created': ('django.db.models.fields.IntegerField', [], {}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.FeedBack']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invalid': ('django.db.models.fields.IntegerField', [], {}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'model_verbose': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'processed': ('django.db.models.fields.IntegerField', [], {}),
            'total': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['catalog']