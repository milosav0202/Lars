# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'GoogleKeywordPerformanceReport', fields ['ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId']
        db.delete_unique('main_googlekeywordperformancereport', ['ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId'])

        # Removing unique constraint on 'GoogleGeoPerformanceReport', fields ['MetroCriteriaId', 'AdGroupId', 'CountryCriteriaId', 'LocationType', 'CityCriteriaId', 'Date', 'ExternalCustomerId', 'RegionCriteriaId']
        db.delete_unique('main_googlegeoperformancereport', ['MetroCriteriaId', 'AdGroupId', 'CountryCriteriaId', 'LocationType', 'CityCriteriaId', 'Date', 'ExternalCustomerId', 'RegionCriteriaId'])

        # Removing unique constraint on 'GoogleAccountPerformanceReport', fields ['ExternalCustomerId', 'Date']
        db.delete_unique('main_googleaccountperformancereport', ['ExternalCustomerId', 'Date'])

        # Removing unique constraint on 'GoogleCampaignPerformanceReport', fields ['ExternalCustomerId', 'Date', 'CampaignId']
        db.delete_unique('main_googlecampaignperformancereport', ['ExternalCustomerId', 'Date', 'CampaignId'])

        # Adding unique constraint on 'GoogleCampaignPerformanceReport', fields ['AdNetworkType2', 'ClickType', 'CampaignId', 'Date', 'AdNetworkType1', 'ExternalCustomerId']
        db.create_unique('main_googlecampaignperformancereport', ['AdNetworkType2', 'ClickType', 'CampaignId', 'Date', 'AdNetworkType1', 'ExternalCustomerId'])

        # Adding unique constraint on 'GoogleAccountPerformanceReport', fields ['AdNetworkType2', 'ClickType', 'Device', 'Date', 'AdNetworkType1', 'ExternalCustomerId']
        db.create_unique('main_googleaccountperformancereport', ['AdNetworkType2', 'ClickType', 'Device', 'Date', 'AdNetworkType1', 'ExternalCustomerId'])

        # Adding unique constraint on 'GoogleGeoPerformanceReport', fields ['MetroCriteriaId', 'AdGroupId', 'CountryCriteriaId', 'AdNetworkType2', 'LocationType', 'CityCriteriaId', 'Device', 'Date', 'AdNetworkType1', 'ExternalCustomerId', 'RegionCriteriaId']
        db.create_unique('main_googlegeoperformancereport', ['MetroCriteriaId', 'AdGroupId', 'CountryCriteriaId', 'AdNetworkType2', 'LocationType', 'CityCriteriaId', 'Device', 'Date', 'AdNetworkType1', 'ExternalCustomerId', 'RegionCriteriaId'])

        # Adding unique constraint on 'GoogleKeywordPerformanceReport', fields ['AdGroupId', 'AdNetworkType2', 'ClickType', 'Device', 'Date', 'AdNetworkType1', 'KeywordId', 'ExternalCustomerId']
        db.create_unique('main_googlekeywordperformancereport', ['AdGroupId', 'AdNetworkType2', 'ClickType', 'Device', 'Date', 'AdNetworkType1', 'KeywordId', 'ExternalCustomerId'])


    def backwards(self, orm):
        # Removing unique constraint on 'GoogleKeywordPerformanceReport', fields ['AdGroupId', 'AdNetworkType2', 'ClickType', 'Device', 'Date', 'AdNetworkType1', 'KeywordId', 'ExternalCustomerId']
        db.delete_unique('main_googlekeywordperformancereport', ['AdGroupId', 'AdNetworkType2', 'ClickType', 'Device', 'Date', 'AdNetworkType1', 'KeywordId', 'ExternalCustomerId'])

        # Removing unique constraint on 'GoogleGeoPerformanceReport', fields ['MetroCriteriaId', 'AdGroupId', 'CountryCriteriaId', 'AdNetworkType2', 'LocationType', 'CityCriteriaId', 'Device', 'Date', 'AdNetworkType1', 'ExternalCustomerId', 'RegionCriteriaId']
        db.delete_unique('main_googlegeoperformancereport', ['MetroCriteriaId', 'AdGroupId', 'CountryCriteriaId', 'AdNetworkType2', 'LocationType', 'CityCriteriaId', 'Device', 'Date', 'AdNetworkType1', 'ExternalCustomerId', 'RegionCriteriaId'])

        # Removing unique constraint on 'GoogleAccountPerformanceReport', fields ['AdNetworkType2', 'ClickType', 'Device', 'Date', 'AdNetworkType1', 'ExternalCustomerId']
        db.delete_unique('main_googleaccountperformancereport', ['AdNetworkType2', 'ClickType', 'Device', 'Date', 'AdNetworkType1', 'ExternalCustomerId'])

        # Removing unique constraint on 'GoogleCampaignPerformanceReport', fields ['AdNetworkType2', 'ClickType', 'CampaignId', 'Date', 'AdNetworkType1', 'ExternalCustomerId']
        db.delete_unique('main_googlecampaignperformancereport', ['AdNetworkType2', 'ClickType', 'CampaignId', 'Date', 'AdNetworkType1', 'ExternalCustomerId'])

        # Adding unique constraint on 'GoogleCampaignPerformanceReport', fields ['ExternalCustomerId', 'Date', 'CampaignId']
        db.create_unique('main_googlecampaignperformancereport', ['ExternalCustomerId', 'Date', 'CampaignId'])

        # Adding unique constraint on 'GoogleAccountPerformanceReport', fields ['ExternalCustomerId', 'Date']
        db.create_unique('main_googleaccountperformancereport', ['ExternalCustomerId', 'Date'])

        # Adding unique constraint on 'GoogleGeoPerformanceReport', fields ['MetroCriteriaId', 'AdGroupId', 'CountryCriteriaId', 'LocationType', 'CityCriteriaId', 'Date', 'ExternalCustomerId', 'RegionCriteriaId']
        db.create_unique('main_googlegeoperformancereport', ['MetroCriteriaId', 'AdGroupId', 'CountryCriteriaId', 'LocationType', 'CityCriteriaId', 'Date', 'ExternalCustomerId', 'RegionCriteriaId'])

        # Adding unique constraint on 'GoogleKeywordPerformanceReport', fields ['ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId']
        db.create_unique('main_googlekeywordperformancereport', ['ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId'])


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
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'AdNetworkType1', 'AdNetworkType2', 'Device', 'ClickType'),)", 'object_name': 'GoogleAccountPerformanceReport'},
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
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'CampaignId', 'AdNetworkType1', 'AdNetworkType2', 'ClickType'),)", 'object_name': 'GoogleCampaignPerformanceReport'},
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
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'AdGroupId', 'LocationType', 'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId', 'AdNetworkType1', 'AdNetworkType2', 'Device'),)", 'object_name': 'GoogleGeoPerformanceReport'},
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
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'AdGroupId', 'KeywordId', 'AdNetworkType1', 'AdNetworkType2', 'Device', 'ClickType'),)", 'object_name': 'GoogleKeywordPerformanceReport'},
            'TotalConvValue': ('django.db.models.fields.FloatField', [], {}),
            'ValuePerConversion': ('django.db.models.fields.FloatField', [], {}),
            'ViewThroughConversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']