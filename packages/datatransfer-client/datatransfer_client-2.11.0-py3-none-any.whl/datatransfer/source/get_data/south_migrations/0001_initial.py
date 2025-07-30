# -*- coding: utf-8 -*-
from __future__ import absolute_import
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GetDataSession'
        db.create_table('get_data_getdatasession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('session', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('get_data', ['GetDataSession'])

        # Adding model 'GetDataStatistic'
        db.create_table('get_data_getdatastatistic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['get_data.GetDataSession'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('get_data', ['GetDataStatistic'])

        # Adding model 'GetDataPerson'
        db.create_table('get_data_getdataperson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('local_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('regional_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('source_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('external_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('federal_id', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['get_data.GetDataSession'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(blank=True, null=True)),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('snils', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('health_group', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('long_term_treatment', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('disability_group', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('disability_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('disability_reason', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('adaptation_program', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('physical_culture_group', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('difficult_situation', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('document_registry_number', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('document_registry_issuer', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('document_registry_issue_date', self.gf('django.db.models.fields.DateField')(blank=True, null=True)),
            ('citizenship', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('registration_address_place', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('registration_address_street', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('registration_address_house', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('registration_address_flat', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('registration_address', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('residence_address_place', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('residence_address_street', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('residence_address_house', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('residence_address_flat', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('residence_address', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('actual_address_place', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('actual_address_street', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('actual_address_house', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('actual_address_flat', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('actual_address', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('get_data', ['GetDataPerson'])

        # Adding model 'GetDataPersonDocument'
        db.create_table('get_data_getdatapersondocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('local_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['get_data.GetDataPerson'])),
            ('regional_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('source_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('external_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['get_data.GetDataSession'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('issuer', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True, null=True)),
            ('issue_date', self.gf('django.db.models.fields.DateField')(blank=True, null=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('get_data', ['GetDataPersonDocument'])

        # Adding model 'GetDataChanges'
        db.create_table('get_data_getdatachanges', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['get_data.GetDataSession'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='getdatachangesmodel', to=orm['contenttypes.ContentType'])),
            ('local_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('applied', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user_model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='getdatachangesusermodel', to=orm['contenttypes.ContentType'])),
            ('user_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('data', self.gf('django.db.models.fields.TextField')(max_length=4096)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('get_data', ['GetDataChanges'])


    def backwards(self, orm):
        # Deleting model 'GetDataSession'
        db.delete_table('get_data_getdatasession')

        # Deleting model 'GetDataStatistic'
        db.delete_table('get_data_getdatastatistic')

        # Deleting model 'GetDataPerson'
        db.delete_table('get_data_getdataperson')

        # Deleting model 'GetDataPersonDocument'
        db.delete_table('get_data_getdatapersondocument')

        # Deleting model 'GetDataChanges'
        db.delete_table('get_data_getdatachanges')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'get_data.getdatachanges': {
            'Meta': {'object_name': 'GetDataChanges'},
            'applied': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'data': ('django.db.models.fields.TextField', [], {'max_length': '4096'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'getdatachangesmodel'", 'to': "orm['contenttypes.ContentType']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['get_data.GetDataSession']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'user_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'user_model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'getdatachangesusermodel'", 'to': "orm['contenttypes.ContentType']"})
        },
        'get_data.getdataperson': {
            'Meta': {'object_name': 'GetDataPerson'},
            'actual_address': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'actual_address_flat': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'actual_address_house': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'actual_address_place': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'actual_address_street': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'adaptation_program': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'citizenship': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'difficult_situation': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'disability_expiration_date': ('django.db.models.fields.DateField', [], {}),
            'disability_group': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'disability_reason': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'document_registry_issue_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'document_registry_issuer': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'document_registry_number': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'federal_id': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'health_group': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'local_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'long_term_treatment': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'physical_culture_group': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'regional_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'registration_address': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'registration_address_flat': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'registration_address_house': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'registration_address_place': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'registration_address_street': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'residence_address': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'residence_address_flat': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'residence_address_house': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'residence_address_place': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'residence_address_street': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['get_data.GetDataSession']"}),
            'snils': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'source_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'get_data.getdatapersondocument': {
            'Meta': {'object_name': 'GetDataPersonDocument'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'external_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'issuer': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'local_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['get_data.GetDataPerson']"}),
            'regional_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['get_data.GetDataSession']"}),
            'source_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'})
        },
        'get_data.getdatasession': {
            'Meta': {'object_name': 'GetDataSession'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'get_data.getdatastatistic': {
            'Meta': {'object_name': 'GetDataStatistic'},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['get_data.GetDataSession']"})
        }
    }

    complete_apps = ['get_data']