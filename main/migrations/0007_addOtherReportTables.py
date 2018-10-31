# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GoogleCampaignPerformanceReport'
        db.create_table('main_googlecampaignperformancereport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ExternalCustomerId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('Date', self.gf('django.db.models.fields.DateField')()),
            ('AccountDescriptiveName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('AccountCurrencyCode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('AccountId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('AccountTimeZoneId', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('CampaignId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('CampaignName', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('CampaignStatus', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('Impressions', self.gf('django.db.models.fields.BigIntegerField')()),
            ('Clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('Ctr', self.gf('django.db.models.fields.FloatField')()),
            ('AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('AveragePosition', self.gf('django.db.models.fields.FloatField')()),
            ('Conversions', self.gf('django.db.models.fields.BigIntegerField')()),
            ('CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('ConversionRate', self.gf('django.db.models.fields.FloatField')()),
            ('TotalConvValue', self.gf('django.db.models.fields.BigIntegerField')()),
            ('ViewThroughConversions', self.gf('django.db.models.fields.BigIntegerField')()),
            ('ValuePerConversion', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['GoogleCampaignPerformanceReport'])

        # Adding unique constraint on 'GoogleCampaignPerformanceReport', fields ['ExternalCustomerId', 'Date', 'CampaignId']
        db.create_unique('main_googlecampaignperformancereport', ['ExternalCustomerId', 'Date', 'CampaignId'])

        # Adding model 'GoogleGeoPerformanceReport'
        db.create_table('main_googlegeoperformancereport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ExternalCustomerId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('Date', self.gf('django.db.models.fields.DateField')()),
            ('AccountDescriptiveName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('AccountCurrencyCode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('AccountTimeZoneId', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('CampaignId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('CampaignName', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('CampaignStatus', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('AdGroupId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('AdGroupName', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('AdGroupStatus', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('LocationType', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('CountryCriteriaId', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('RegionCriteriaId', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('MetroCriteriaId', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('CityCriteriaId', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('Impressions', self.gf('django.db.models.fields.BigIntegerField')()),
            ('Clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('Ctr', self.gf('django.db.models.fields.FloatField')()),
            ('AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('AveragePosition', self.gf('django.db.models.fields.FloatField')()),
            ('Conversions', self.gf('django.db.models.fields.BigIntegerField')()),
            ('CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('ConversionRate', self.gf('django.db.models.fields.FloatField')()),
            ('TotalConvValue', self.gf('django.db.models.fields.BigIntegerField')()),
            ('ViewThroughConversions', self.gf('django.db.models.fields.BigIntegerField')()),
            ('ValuePerConversion', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['GoogleGeoPerformanceReport'])

        # Adding unique constraint on 'GoogleGeoPerformanceReport', fields ['ExternalCustomerId', 'Date', 'AdGroupId', 'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId']
        db.create_unique('main_googlegeoperformancereport', ['ExternalCustomerId', 'Date', 'AdGroupId', 'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId'])

        # Adding model 'GoogleKeywordPerformanceReport'
        db.create_table('main_googlekeywordperformancereport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ExternalCustomerId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('Date', self.gf('django.db.models.fields.DateField')()),
            ('AccountDescriptiveName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('AccountCurrencyCode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('AccountTimeZoneId', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('CampaignId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('CampaignName', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('CampaignStatus', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('AdGroupId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('AdGroupName', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('AdGroupStatus', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('KeywordId', self.gf('django.db.models.fields.BigIntegerField')()),
            ('KeywordText', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('KeywordMatchType', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('Impressions', self.gf('django.db.models.fields.BigIntegerField')()),
            ('Clicks', self.gf('django.db.models.fields.IntegerField')()),
            ('Ctr', self.gf('django.db.models.fields.FloatField')()),
            ('AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('AveragePosition', self.gf('django.db.models.fields.FloatField')()),
            ('Conversions', self.gf('django.db.models.fields.BigIntegerField')()),
            ('CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('ConversionRate', self.gf('django.db.models.fields.FloatField')()),
            ('TotalConvValue', self.gf('django.db.models.fields.BigIntegerField')()),
            ('ViewThroughConversions', self.gf('django.db.models.fields.BigIntegerField')()),
            ('ValuePerConversion', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['GoogleKeywordPerformanceReport'])

        # Adding unique constraint on 'GoogleKeywordPerformanceReport', fields ['ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId']
        db.create_unique('main_googlekeywordperformancereport', ['ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId'])


    def backwards(self, orm):
        # Removing unique constraint on 'GoogleKeywordPerformanceReport', fields ['ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId']
        db.delete_unique('main_googlekeywordperformancereport', ['ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId'])

        # Removing unique constraint on 'GoogleGeoPerformanceReport', fields ['ExternalCustomerId', 'Date', 'AdGroupId', 'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId']
        db.delete_unique('main_googlegeoperformancereport', ['ExternalCustomerId', 'Date', 'AdGroupId', 'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId'])

        # Removing unique constraint on 'GoogleCampaignPerformanceReport', fields ['ExternalCustomerId', 'Date', 'CampaignId']
        db.delete_unique('main_googlecampaignperformancereport', ['ExternalCustomerId', 'Date', 'CampaignId'])

        # Deleting model 'GoogleCampaignPerformanceReport'
        db.delete_table('main_googlecampaignperformancereport')

        # Deleting model 'GoogleGeoPerformanceReport'
        db.delete_table('main_googlegeoperformancereport')

        # Deleting model 'GoogleKeywordPerformanceReport'
        db.delete_table('main_googlekeywordperformancereport')


    models = {
        'main.googleaccountperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountId': ('django.db.models.fields.BigIntegerField', [], {}),
            'AccountTimeZoneId': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'ExternalCustomerId': ('django.db.models.fields.BigIntegerField', [], {}),
            'Impressions': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date'),)", 'object_name': 'GoogleAccountPerformanceReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.googlecampaignperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountId': ('django.db.models.fields.BigIntegerField', [], {}),
            'AccountTimeZoneId': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'CampaignId': ('django.db.models.fields.BigIntegerField', [], {}),
            'CampaignName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'CampaignStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'ConversionRate': ('django.db.models.fields.FloatField', [], {}),
            'Conversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'CostPerConversion': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'ExternalCustomerId': ('django.db.models.fields.BigIntegerField', [], {}),
            'Impressions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'CampaignId'),)", 'object_name': 'GoogleCampaignPerformanceReport'},
            'TotalConvValue': ('django.db.models.fields.BigIntegerField', [], {}),
            'ValuePerConversion': ('django.db.models.fields.FloatField', [], {}),
            'ViewThroughConversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.googlegeoperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountTimeZoneId': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'AdGroupId': ('django.db.models.fields.BigIntegerField', [], {}),
            'AdGroupName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'AdGroupStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'CampaignId': ('django.db.models.fields.BigIntegerField', [], {}),
            'CampaignName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'CampaignStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'CityCriteriaId': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'ConversionRate': ('django.db.models.fields.FloatField', [], {}),
            'Conversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'CostPerConversion': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'CountryCriteriaId': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'ExternalCustomerId': ('django.db.models.fields.BigIntegerField', [], {}),
            'Impressions': ('django.db.models.fields.BigIntegerField', [], {}),
            'LocationType': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'AdGroupId', 'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId'),)", 'object_name': 'GoogleGeoPerformanceReport'},
            'MetroCriteriaId': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'RegionCriteriaId': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'TotalConvValue': ('django.db.models.fields.BigIntegerField', [], {}),
            'ValuePerConversion': ('django.db.models.fields.FloatField', [], {}),
            'ViewThroughConversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.googlekeywordperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountTimeZoneId': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'AdGroupId': ('django.db.models.fields.BigIntegerField', [], {}),
            'AdGroupName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'AdGroupStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'CampaignId': ('django.db.models.fields.BigIntegerField', [], {}),
            'CampaignName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'CampaignStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'ConversionRate': ('django.db.models.fields.FloatField', [], {}),
            'Conversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'CostPerConversion': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'ExternalCustomerId': ('django.db.models.fields.BigIntegerField', [], {}),
            'Impressions': ('django.db.models.fields.BigIntegerField', [], {}),
            'KeywordId': ('django.db.models.fields.BigIntegerField', [], {}),
            'KeywordMatchType': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'KeywordText': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId'),)", 'object_name': 'GoogleKeywordPerformanceReport'},
            'TotalConvValue': ('django.db.models.fields.BigIntegerField', [], {}),
            'ValuePerConversion': ('django.db.models.fields.FloatField', [], {}),
            'ViewThroughConversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']