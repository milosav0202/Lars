# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'RawReportGoogle'
        db.delete_table('main_rawreportgoogle')

        # Adding model 'GoogleAccountPerformanceReport'
        db.create_table('main_googleaccountperformancereport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('AccountDescriptiveName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('Date', self.gf('django.db.models.fields.DateField')()),
            ('AccountCurrencyCode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('AccountId', self.gf('django.db.models.fields.IntegerField')()),
            ('AccountTimeZoneId', self.gf('django.db.models.fields.IntegerField')()),
            ('Impressions', self.gf('django.db.models.fields.IntegerField')()),
            ('Clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('Ctr', self.gf('django.db.models.fields.FloatField')()),
            ('AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('AveragePosition', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['GoogleAccountPerformanceReport'])


    def backwards(self, orm):
        # Adding model 'RawReportGoogle'
        db.create_table('main_rawreportgoogle', (
            ('Ctr', self.gf('django.db.models.fields.FloatField')()),
            ('Clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('AccountTimeZoneId', self.gf('django.db.models.fields.IntegerField')()),
            ('AveragePosition', self.gf('django.db.models.fields.FloatField')()),
            ('AccountCurrencyCode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('AccountDescriptiveName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('Date', self.gf('django.db.models.fields.DateField')()),
            ('Impressions', self.gf('django.db.models.fields.IntegerField')()),
            ('AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('AccountId', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['RawReportGoogle'])

        # Deleting model 'GoogleAccountPerformanceReport'
        db.delete_table('main_googleaccountperformancereport')


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
            'Meta': {'object_name': 'GoogleAccountPerformanceReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']