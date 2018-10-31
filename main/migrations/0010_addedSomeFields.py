# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GoogleCampaignPerformanceReport.AdNetworkType1'
        db.add_column('main_googlecampaignperformancereport', 'AdNetworkType1',
                      self.gf('django.db.models.fields.CharField')(default='s', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleCampaignPerformanceReport.AdNetworkType2'
        db.add_column('main_googlecampaignperformancereport', 'AdNetworkType2',
                      self.gf('django.db.models.fields.CharField')(default='s', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleCampaignPerformanceReport.ClickType'
        db.add_column('main_googlecampaignperformancereport', 'ClickType',
                      self.gf('django.db.models.fields.CharField')(default='s', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleAccountPerformanceReport.AdNetworkType1'
        db.add_column('main_googleaccountperformancereport', 'AdNetworkType1',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleAccountPerformanceReport.AdNetworkType2'
        db.add_column('main_googleaccountperformancereport', 'AdNetworkType2',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleAccountPerformanceReport.Device'
        db.add_column('main_googleaccountperformancereport', 'Device',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleAccountPerformanceReport.ClickType'
        db.add_column('main_googleaccountperformancereport', 'ClickType',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleGeoPerformanceReport.AdNetworkType1'
        db.add_column('main_googlegeoperformancereport', 'AdNetworkType1',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleGeoPerformanceReport.AdNetworkType2'
        db.add_column('main_googlegeoperformancereport', 'AdNetworkType2',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleGeoPerformanceReport.Device'
        db.add_column('main_googlegeoperformancereport', 'Device',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleKeywordPerformanceReport.AdNetworkType1'
        db.add_column('main_googlekeywordperformancereport', 'AdNetworkType1',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleKeywordPerformanceReport.AdNetworkType2'
        db.add_column('main_googlekeywordperformancereport', 'AdNetworkType2',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleKeywordPerformanceReport.Device'
        db.add_column('main_googlekeywordperformancereport', 'Device',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)

        # Adding field 'GoogleKeywordPerformanceReport.ClickType'
        db.add_column('main_googlekeywordperformancereport', 'ClickType',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GoogleCampaignPerformanceReport.AdNetworkType1'
        db.delete_column('main_googlecampaignperformancereport', 'AdNetworkType1')

        # Deleting field 'GoogleCampaignPerformanceReport.AdNetworkType2'
        db.delete_column('main_googlecampaignperformancereport', 'AdNetworkType2')

        # Deleting field 'GoogleCampaignPerformanceReport.ClickType'
        db.delete_column('main_googlecampaignperformancereport', 'ClickType')

        # Deleting field 'GoogleAccountPerformanceReport.AdNetworkType1'
        db.delete_column('main_googleaccountperformancereport', 'AdNetworkType1')

        # Deleting field 'GoogleAccountPerformanceReport.AdNetworkType2'
        db.delete_column('main_googleaccountperformancereport', 'AdNetworkType2')

        # Deleting field 'GoogleAccountPerformanceReport.Device'
        db.delete_column('main_googleaccountperformancereport', 'Device')

        # Deleting field 'GoogleAccountPerformanceReport.ClickType'
        db.delete_column('main_googleaccountperformancereport', 'ClickType')

        # Deleting field 'GoogleGeoPerformanceReport.AdNetworkType1'
        db.delete_column('main_googlegeoperformancereport', 'AdNetworkType1')

        # Deleting field 'GoogleGeoPerformanceReport.AdNetworkType2'
        db.delete_column('main_googlegeoperformancereport', 'AdNetworkType2')

        # Deleting field 'GoogleGeoPerformanceReport.Device'
        db.delete_column('main_googlegeoperformancereport', 'Device')

        # Deleting field 'GoogleKeywordPerformanceReport.AdNetworkType1'
        db.delete_column('main_googlekeywordperformancereport', 'AdNetworkType1')

        # Deleting field 'GoogleKeywordPerformanceReport.AdNetworkType2'
        db.delete_column('main_googlekeywordperformancereport', 'AdNetworkType2')

        # Deleting field 'GoogleKeywordPerformanceReport.Device'
        db.delete_column('main_googlekeywordperformancereport', 'Device')

        # Deleting field 'GoogleKeywordPerformanceReport.ClickType'
        db.delete_column('main_googlekeywordperformancereport', 'ClickType')


    models = {
        'main.googleaccountperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountId': ('django.db.models.fields.BigIntegerField', [], {}),
            'AccountTimeZoneId': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'AdNetworkType1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AdNetworkType2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'ClickType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'Device': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'AdNetworkType1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AdNetworkType2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'CampaignId': ('django.db.models.fields.BigIntegerField', [], {}),
            'CampaignName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'CampaignStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ClickType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'TotalConvValue': ('django.db.models.fields.FloatField', [], {}),
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
            'AdNetworkType1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AdNetworkType2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'Device': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ExternalCustomerId': ('django.db.models.fields.BigIntegerField', [], {}),
            'Impressions': ('django.db.models.fields.BigIntegerField', [], {}),
            'LocationType': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'AdGroupId', 'LocationType', 'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId'),)", 'object_name': 'GoogleGeoPerformanceReport'},
            'MetroCriteriaId': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'RegionCriteriaId': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'TotalConvValue': ('django.db.models.fields.FloatField', [], {}),
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
            'AdNetworkType1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AdNetworkType2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'CampaignId': ('django.db.models.fields.BigIntegerField', [], {}),
            'CampaignName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'CampaignStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ClickType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'ConversionRate': ('django.db.models.fields.FloatField', [], {}),
            'Conversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'CostPerConversion': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'Device': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ExternalCustomerId': ('django.db.models.fields.BigIntegerField', [], {}),
            'Impressions': ('django.db.models.fields.BigIntegerField', [], {}),
            'KeywordId': ('django.db.models.fields.BigIntegerField', [], {}),
            'KeywordMatchType': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'KeywordText': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId'),)", 'object_name': 'GoogleKeywordPerformanceReport'},
            'TotalConvValue': ('django.db.models.fields.FloatField', [], {}),
            'ValuePerConversion': ('django.db.models.fields.FloatField', [], {}),
            'ViewThroughConversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']