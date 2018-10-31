# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Account', fields ['ServiceType', 'ServiceAccountId']
        db.delete_unique(u'main_account', ['ServiceType', 'ServiceAccountId'])

        # Deleting model 'Account'
        db.delete_table(u'main_account')

        # Deleting model 'Group'
        db.delete_table(u'main_group')


        # Changing field 'GoogleCampaignPerformanceReport.CostPerConversion'
        db.alter_column(u'main_googlecampaignperformancereport', 'CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleCampaignPerformanceReport.Cost'
        db.alter_column(u'main_googlecampaignperformancereport', 'Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleCampaignPerformanceReport.AverageCpc'
        db.alter_column(u'main_googlecampaignperformancereport', 'AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleGeoPerformanceReport.CostPerConversion'
        db.alter_column(u'main_googlegeoperformancereport', 'CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleGeoPerformanceReport.Cost'
        db.alter_column(u'main_googlegeoperformancereport', 'Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleGeoPerformanceReport.AverageCpc'
        db.alter_column(u'main_googlegeoperformancereport', 'AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleKeywordPerformanceReport.CostPerConversion'
        db.alter_column(u'main_googlekeywordperformancereport', 'CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleKeywordPerformanceReport.Cost'
        db.alter_column(u'main_googlekeywordperformancereport', 'Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleKeywordPerformanceReport.AverageCpc'
        db.alter_column(u'main_googlekeywordperformancereport', 'AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'AdAccountOwner.Budget'
        db.alter_column(u'main_adaccountowner', 'Budget', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2))

        # Changing field 'GoogleAccountPerformanceReport.CostPerConversion'
        db.alter_column(u'main_googleaccountperformancereport', 'CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleAccountPerformanceReport.Cost'
        db.alter_column(u'main_googleaccountperformancereport', 'Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

        # Changing field 'GoogleAccountPerformanceReport.AverageCpc'
        db.alter_column(u'main_googleaccountperformancereport', 'AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2))

    def backwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'main_account', (
            ('ServiceType', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('Group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Group'])),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('InternalId', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('Active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ServiceAccountId', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['Account'])

        # Adding unique constraint on 'Account', fields ['ServiceType', 'ServiceAccountId']
        db.create_unique(u'main_account', ['ServiceType', 'ServiceAccountId'])

        # Adding model 'Group'
        db.create_table(u'main_group', (
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('Geo_MetroArea', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('Budget', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('BudgetCurrency', self.gf('django.db.models.fields.CharField')(default='USD', max_length=5)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('MasterAccount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.MasterAccount'])),
        ))
        db.send_create_signal('main', ['Group'])


        # Changing field 'GoogleCampaignPerformanceReport.CostPerConversion'
        db.alter_column(u'main_googlecampaignperformancereport', 'CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleCampaignPerformanceReport.Cost'
        db.alter_column(u'main_googlecampaignperformancereport', 'Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleCampaignPerformanceReport.AverageCpc'
        db.alter_column(u'main_googlecampaignperformancereport', 'AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleGeoPerformanceReport.CostPerConversion'
        db.alter_column(u'main_googlegeoperformancereport', 'CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleGeoPerformanceReport.Cost'
        db.alter_column(u'main_googlegeoperformancereport', 'Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleGeoPerformanceReport.AverageCpc'
        db.alter_column(u'main_googlegeoperformancereport', 'AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleKeywordPerformanceReport.CostPerConversion'
        db.alter_column(u'main_googlekeywordperformancereport', 'CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleKeywordPerformanceReport.Cost'
        db.alter_column(u'main_googlekeywordperformancereport', 'Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleKeywordPerformanceReport.AverageCpc'
        db.alter_column(u'main_googlekeywordperformancereport', 'AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'AdAccountOwner.Budget'
        db.alter_column(u'main_adaccountowner', 'Budget', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2))

        # Changing field 'GoogleAccountPerformanceReport.CostPerConversion'
        db.alter_column(u'main_googleaccountperformancereport', 'CostPerConversion', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleAccountPerformanceReport.Cost'
        db.alter_column(u'main_googleaccountperformancereport', 'Cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'GoogleAccountPerformanceReport.AverageCpc'
        db.alter_column(u'main_googleaccountperformancereport', 'AverageCpc', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

    models = {
        u'main.adaccount': {
            'Active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'Meta': {'unique_together': "(('ServiceType', 'ServiceAccountId'),)", 'object_name': 'AdAccount'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'ServiceAccountId': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'ServiceType': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.adaccountgrouping': {
            'Meta': {'object_name': 'AdAccountGrouping'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parentaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subaccounts'", 'to': u"orm['main.AdAccountOwner']"}),
            'subaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parental'", 'unique': 'True', 'to': u"orm['main.AdAccountOwner']"})
        },
        u'main.adaccountowner': {
            'Active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'Budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'BudgetCurrency': ('django.db.models.fields.CharField', [], {'default': "'USD'", 'max_length': '5'}),
            'Geo_MetroArea': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'InternalId': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'MasterAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.MasterAccount']"}),
            'Meta': {'ordering': "['MasterAccount', 'Name']", 'object_name': 'AdAccountOwner'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.adaccountownership': {
            'AdAccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'unique': 'True', 'to': u"orm['main.AdAccount']"}),
            'AdAccountOwner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adaccounts'", 'to': u"orm['main.AdAccountOwner']"}),
            'Meta': {'object_name': 'AdAccountOwnership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.agemaillog': {
            'Meta': {'object_name': 'AGEmailLog'},
            'Rid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ServerDateTime': ('django.db.models.fields.DateTimeField', [], {}),
            'ServerTime': ('django.db.models.fields.DateField', [], {}),
            'StoreNum': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        u'main.googleaccountperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountId': ('django.db.models.fields.BigIntegerField', [], {}),
            'AccountTimeZoneId': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'AdNetworkType1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AdNetworkType2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'ClickType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'ConversionRate': ('django.db.models.fields.FloatField', [], {}),
            'Conversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'CostPerConversion': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'Device': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ExternalCustomerId': ('django.db.models.fields.BigIntegerField', [], {}),
            'Impressions': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'AdNetworkType1', 'AdNetworkType2', 'Device', 'ClickType'),)", 'object_name': 'GoogleAccountPerformanceReport'},
            'TotalConvValue': ('django.db.models.fields.FloatField', [], {}),
            'ValuePerConversion': ('django.db.models.fields.FloatField', [], {}),
            'ViewThroughConversions': ('django.db.models.fields.BigIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.googlecampaignperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountId': ('django.db.models.fields.BigIntegerField', [], {}),
            'AccountTimeZoneId': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'AdNetworkType1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AdNetworkType2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'CampaignId': ('django.db.models.fields.BigIntegerField', [], {}),
            'CampaignName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'CampaignStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ClickType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'ConversionRate': ('django.db.models.fields.FloatField', [], {}),
            'Conversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'CostPerConversion': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'Ctr': ('django.db.models.fields.FloatField', [], {}),
            'Date': ('django.db.models.fields.DateField', [], {}),
            'ExternalCustomerId': ('django.db.models.fields.BigIntegerField', [], {}),
            'Impressions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Meta': {'unique_together': "(('ExternalCustomerId', 'Date', 'CampaignId', 'AdNetworkType1', 'AdNetworkType2', 'ClickType'),)", 'object_name': 'GoogleCampaignPerformanceReport'},
            'TotalConvValue': ('django.db.models.fields.FloatField', [], {}),
            'ValuePerConversion': ('django.db.models.fields.FloatField', [], {}),
            'ViewThroughConversions': ('django.db.models.fields.BigIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.googlegeoperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountTimeZoneId': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'AdGroupId': ('django.db.models.fields.BigIntegerField', [], {}),
            'AdGroupName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'AdGroupStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'AdNetworkType1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AdNetworkType2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'CampaignId': ('django.db.models.fields.BigIntegerField', [], {}),
            'CampaignName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'CampaignStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'CityCriteriaId': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'ConversionRate': ('django.db.models.fields.FloatField', [], {}),
            'Conversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'CostPerConversion': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.googlekeywordperformancereport': {
            'AccountCurrencyCode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'AccountDescriptiveName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'AccountTimeZoneId': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'AdGroupId': ('django.db.models.fields.BigIntegerField', [], {}),
            'AdGroupName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'AdGroupStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'AdNetworkType1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AdNetworkType2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'AverageCpc': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'AveragePosition': ('django.db.models.fields.FloatField', [], {}),
            'CampaignId': ('django.db.models.fields.BigIntegerField', [], {}),
            'CampaignName': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'CampaignStatus': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ClickType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'Clicks': ('django.db.models.fields.IntegerField', [], {}),
            'ConversionRate': ('django.db.models.fields.FloatField', [], {}),
            'Conversions': ('django.db.models.fields.BigIntegerField', [], {}),
            'Cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'CostPerConversion': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.masteraccount': {
            'Meta': {'object_name': 'MasterAccount'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.metroarea': {
            'DMACode': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'object_name': 'MetroArea'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.voicestarcalllog': {
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbound_ext': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'inbound_no': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'listenedto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        }
    }

    complete_apps = ['main']