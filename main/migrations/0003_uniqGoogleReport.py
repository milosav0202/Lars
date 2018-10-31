# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'GoogleAccountPerformanceReport', fields ['Date', 'AccountId']
        db.create_unique('main_googleaccountperformancereport', ['Date', 'AccountId'])


    def backwards(self, orm):
        # Removing unique constraint on 'GoogleAccountPerformanceReport', fields ['Date', 'AccountId']
        db.delete_unique('main_googleaccountperformancereport', ['Date', 'AccountId'])


    models = {
        'main.googleaccountperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountId': ('django.db.models.fields.IntegerField', [], {}),
            'AccountTimeZoneId': ('django.db.models.fields.IntegerField', [], {}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'Impressions': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'unique_together': "(('AccountId', 'Date'),)", 'object_name': 'GoogleAccountPerformanceReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']