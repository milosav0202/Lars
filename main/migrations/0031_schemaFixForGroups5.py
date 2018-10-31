# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AdAccount.AdAccountOwner'
        db.delete_column('main_adaccount', 'AdAccountOwner_id')

        # Deleting field 'AdAccountOwner.parent'
        db.delete_column('main_adaccountowner', 'parent_id')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'AdAccount.AdAccountOwner'
        raise RuntimeError("Cannot reverse this migration. 'AdAccount.AdAccountOwner' and its values cannot be restored.")
        # Adding field 'AdAccountOwner.parent'
        db.add_column('main_adaccountowner', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.AdAccountOwner'], null=True, blank=True),
                      keep_default=False)


    models = {
        'main.account': {
            'Active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'Group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Group']"}),
            'InternalId': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'Meta': {'ordering': "['Group', 'Name']", 'unique_together': "(('ServiceType', 'ServiceAccountId'),)", 'object_name': 'Account'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'ServiceAccountId': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'ServiceType': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.adaccount': {
            'Active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'Meta': {'unique_together': "(('ServiceType', 'ServiceAccountId'),)", 'object_name': 'AdAccount'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'ServiceAccountId': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'ServiceType': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.adaccountgrouping': {
            'Meta': {'object_name': 'AdAccountGrouping'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parentaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subaccounts'", 'to': "orm['main.AdAccountOwner']"}),
            'subaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parental'", 'unique': 'True', 'to': "orm['main.AdAccountOwner']"})
        },
        'main.adaccountowner': {
            'Budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'BudgetCurrency': ('django.db.models.fields.CharField', [], {'default': "'USD'", 'max_length': '5'}),
            'Geo_MetroArea': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'InternalId': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'MasterAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.MasterAccount']"}),
            'Meta': {'ordering': "['MasterAccount', 'Name']", 'object_name': 'AdAccountOwner'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.adaccountownership': {
            'AdAccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'unique': 'True', 'to': "orm['main.AdAccount']"}),
            'AdAccountOwner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adaccounts'", 'to': "orm['main.AdAccountOwner']"}),
            'Meta': {'object_name': 'AdAccountOwnership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.agemaillog': {
            'Meta': {'object_name': 'AGEmailLog'},
            'Rid': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'ServerTime': ('django.db.models.fields.DateField', [], {}),
            'StoreNum': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'misc1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'misc2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'misc3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'misc4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'misc5': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'offer': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'projectdetails': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'projectduedate': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'projectname': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'submit': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
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
            'ConversionRate': ('django.db.models.fields.FloatField', [], {}),
            'Conversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'CostPerConversion': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'Device': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ExternalCustomerId': ('django.db.models.fields.BigIntegerField', [], {}),
            'Impressions': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'AdNetworkType1', 'AdNetworkType2', 'Device', 'ClickType'),)", 'object_name': 'GoogleAccountPerformanceReport'},
            'TotalConvValue': ('django.db.models.fields.FloatField', [], {}),
            'ValuePerConversion': ('django.db.models.fields.FloatField', [], {}),
            'ViewThroughConversions': ('django.db.models.fields.BigIntegerField', [], {}),
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
        },
        'main.group': {
            'Budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'BudgetCurrency': ('django.db.models.fields.CharField', [], {'default': "'USD'", 'max_length': '5'}),
            'Geo_MetroArea': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'MasterAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.MasterAccount']"}),
            'Meta': {'ordering': "['MasterAccount', 'Name']", 'object_name': 'Group'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.masteraccount': {
            'Meta': {'object_name': 'MasterAccount'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.metroarea': {
            'DMACode': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'object_name': 'MetroArea'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.voicestarcalllog': {
            'Meta': {'object_name': 'VoiceStarCallLog'},
            'a_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'answer_offset': ('django.db.models.fields.IntegerField', [], {}),
            'c_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'call_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'call_s': ('django.db.models.fields.DateTimeField', [], {}),
            'call_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'caller_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'caller_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'campaign_id': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'custom_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'disposition': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'forward_no': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'g_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'group_id': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbound_ext': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'inbound_no': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'listenedto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        }
    }

    complete_apps = ['main']