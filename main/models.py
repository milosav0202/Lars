# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

"""
Hours Log - March
------------------
Server to windows research and trials - 5
Access Coding - 7
Groups/Client table addition - 4

Importing Groups/Client - 5
Admin Setup for Groups/Client editing - 3

Admin
Automation admin - 2
EC2 fixing - 3
Git setup - 0.5

"""

#testing MongoDB
import pymongo
from pymongo import ReadPreference
master = pymongo.Connection(settings.MONGO_HOST, tz_aware=True)

# if settings.MONGO_HOST_RO:
#     slave1 = pymongo.Connection(settings.MONGO_HOST_RO, tz_aware=True, read_preference=ReadPreference.SECONDARY) #, slave_okay=True
#     mongo_con = pymongo.master_slave_connection.MasterSlaveConnection(master, [slave1], tz_aware=True)
#     mongodb = mongo_con[settings.MONGO_DB]
#     mongodb_ro = mongodb
# else:
mongo_con = master
mongodb = mongo_con[settings.MONGO_DB]
#mongodb_ro = mongodb


# from decimal import Decimal
# class CurrencyField(models.DecimalField):
#     __metaclass__ = models.SubfieldBase

#     def to_python(self, value):
#         try:
#            return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
#         except AttributeError:
#            return None

import dmacodes



CURRENCY_CODES = [
#["CurrencyCode","CurrencyName", "CurrencySymbol"]
["AED","United Arab Emirates Dirham",""],
["ARS","Argentine Peso","AR$"],
["AUD","Australian Dollars","$"],
["BGN","Bulgarian Lev",""],
["BND","Brunei Dollar","$"],
["BOB","Bolivian Boliviano",""],
["BRL","Brazilian Real","R$"],
["CAD","Canadian Dollars","$"],
["CHF","Swiss Francs",""],
["CLP","Chilean Peso","CL$"],
["CNY","Yuan Renminbi","¥"],
["COP","Colombian Peso",""],
["CSD","Old Serbian Dinar",""],
["CZK","Czech Koruna",""],
["DEM","Deutsche Marks",""],
["DKK","Denmark Kroner",""],
["EEK","Estonian Kroon",""],
["EGP","Egyptian Pound",""],
["EUR","Euros","€"],
["FJD","Fiji Dollar","$"],
["FRF","French Franks",""],
["GBP","British Pounds Sterling","£"],
["HKD","Hong Kong Dollars","$"],
["HRK","Croatian Kuna",""],
["HUF","Hungarian Forint",""],
["IDR","Indonesian Rupiah",""],
["ILS","Israeli Shekel","₪"],
["INR","Indian Rupee",""],
["JPY","Japanese Yen","¥"],
["KES","Kenyan Shilling",""],
["KRW","South Korean Won","₩"],
["LTL","Lithuanian Litas",""],
["MAD","Moroccan Dirham",""],
["MTL","Maltese Lira",""],
["MXN","Mexico Peso",""],
["MYR","Malaysian Ringgit",""],
["NOK","Norway Kroner",""],
["NZD","New Zealand Dollars","$"],
["PEN","Peruvian Nuevo Sol",""],
["PHP","Philippine Peso",""],
["PKR","Pakistan Rupee",""],
["PLN","Polish New Zloty",""],
["ROL","Romanian Leu",""],
["RON","New Romanian Leu",""],
["RSD","Serbian Dinar",""],
["RUB","Russian Rouble",""],
["SAR","Saudi Riyal",""],
["SEK","Sweden Kronor",""],
["SGD","Singapore Dollars","$"],
["SIT","Slovenian Tolar",""],
["SKK","Slovak Koruna",""],
["THB","Thai Baht","฿"],
["TRL","Turkish Lira",""],
["TRY","New Turkish Lira",""],
["TWD","New Taiwan Dollar","$"],
["UAH","Ukrainian Hryvnia",""],
["USD","US Dollars","$"],
["VEB","Venezuela Bolivar",""],
["VEF","Venezuela Bolivar Fuerte",""],
["VND","Vietnamese Dong","₫"],
["ZAR","South African Rand","R"]
]

D_CURRENCY_CODES = dict()
for lsCodeSet in CURRENCY_CODES:
    D_CURRENCY_CODES[lsCodeSet[0]] = {"CurrencyName":lsCodeSet[1], "CurrencySymbol":lsCodeSet[2]}



class MetroArea(models.Model):
    Name = models.CharField('Client Name', max_length=150)
    DMACode = models.IntegerField("DMA Code", choices=dmacodes.T_DMA_CHOICES)


# class LarsClient(models.Model):
#     Name = models.CharField('Client Name', max_length=120)
#     BudgetCurrency = models.CharField("Budget Currency", max_length=5, default="USD", choices=((k,v["CurrencyName"]) for k,v in D_CURRENCY_CODES.iteritems()) )
#     Budget = models.DecimalField("Budget", max_digits=16, decimal_places=2, blank=True, null=True)

#     def __unicode__(self):
#         return self.Name


class MasterAccount(models.Model):
    Name = models.CharField('Group Name', max_length=120)
    GoogleMCCId = models.CharField('Google MCC ID', max_length=80, blank=True, null=True)
    ## Note: this is the same as the AdAccount Service Account Id
    ##  which actually exists for each MCC.  This is a shortcut.  Ensure that the AdAccount for the MCC
    ##  is assigned to UNKNOWN (id:1)

    def __unicode__(self):
        return self.Name + " (" + self.GoogleMCCId + ")"
    

# class Group(models.Model):
#     MasterAccount = models.ForeignKey(MasterAccount)
#     Name = models.CharField('Group Name', max_length=120)
#     Geo_MetroArea = models.IntegerField("Geo - Metro Area", choices=dmacodes.T_DMA_CHOICES,null=True, blank=True)
#     BudgetCurrency = models.CharField("Budget Currency", max_length=5, default="USD", choices=((k,v["CurrencyName"]) for k,v in D_CURRENCY_CODES.iteritems()) )
#     Budget = models.DecimalField("Budget", max_digits=16, decimal_places=2, blank=True, null=True)

#     def __unicode__(self):
#         sDMA = ""
#         if self.Geo_MetroArea:
#             sDMA = " [DMA: " + MetroArea.objects.get(DMACode__exact=self.Geo_MetroArea).Name + "]"
#         return self.MasterAccount.Name + " - " + self.Name + sDMA

#     class Meta:
#         ordering = ['MasterAccount', 'Name']

T_SERVICETYPE_CHOICES = (('1','Google AdWords'),('2','VoiceStar'),('3','AdCenter'))
D_SERVICETYPE_CHOICES = dict(T_SERVICETYPE_CHOICES)

# class Account(models.Model):
#     Group = models.ForeignKey(Group)
#     Name = models.CharField('Account Name', max_length=120, unique=False)
#     Active = models.BooleanField("Is Active?", default=True)
#     #Shared = models.BooleanField("Is Shared?", default=False)
#     ServiceType = models.CharField("Service Type", max_length=30, choices=(('1','Google AdWords'),('2','VoiceStar'),('3','AdCenter')))  #don't ask why this is char's...
#     ServiceAccountId = models.CharField('Account ID', max_length=80, blank=False)
#     #BudgetCurrency = models.CharField("Budget Currency", max_length=5, default="USD", choices=((k,v["CurrencyName"]) for k,v in D_CURRENCY_CODES.iteritems()) )
#     #Budget = models.DecimalField("Budget", max_digits=16, decimal_places=2, blank=True, null=True)
#     #BudgetDuration = models.ChoiceField("Budget Duration", choices=['Month', 'Day'], default="Month")
#     #Geo_MetroArea = models.IntegerField("Geo - Metro Area", choices=dmacodes.T_DMA_CHOICES,null=True, blank=True)
# #     Geo_StateCode = optional
#     InternalId = models.CharField('Internal ID', max_length=80, blank=True)
    

#     def __unicode__(self):
#         sShared = ""
#         #if self.Shared:
#         #    sShared = " (shared)"
#         return self.Group.Name + " - " + self.Name + "/" + self.get_ServiceType_display() + " (" + self.ServiceAccountId + ")"

#     class Meta:
#         unique_together=(("ServiceType", "ServiceAccountId"))
#         ordering = ['Group', 'Name']


#### new #################

    
    

class AdAccountOwner(models.Model):
    """
    can be either a grouping of accounts or an account
    """
    MasterAccount = models.ForeignKey(MasterAccount)
    Name = models.CharField('Account Name', max_length=120, unique=False)
    Geo_MetroArea = models.IntegerField("Geo - Metro Area", choices=dmacodes.T_DMA_CHOICES,null=True, blank=True)
    BudgetCurrency = models.CharField("Budget Currency", max_length=5, default="USD", choices=((k,v["CurrencyName"]) for k,v in D_CURRENCY_CODES.iteritems()) )
    Budget = models.DecimalField("Budget", max_digits=16, decimal_places=2, blank=True, null=True)
    #parent = models.ForeignKey('AdAccountOwner', blank=True, null=True) #,limit_choices_to = {'MasterAccount_id__exact': self.MasterAccount_id}
    InternalId = models.CharField('Internal ID', max_length=80, blank=True)
    Active = models.BooleanField("Is Active?", default=True)

    def __unicode__(self):
        sDMA = ""
        #if self.Geo_MetroArea:
        #   sDMA = " [DMA: " + MetroArea.objects.get(DMACode__exact=self.Geo_MetroArea).Name + "]"
        return self.MasterAccount.Name + " - " + self.Name + sDMA

    class Meta:
        ordering = ['MasterAccount', 'Name']



class AdAccount(models.Model):
    #AdAccountOwner = models.ForeignKey(AdAccountOwner)
    Name = models.CharField('Account Name', max_length=120, unique=False, blank=True)
    Active = models.BooleanField("Is Active?", default=True)
    #Shared = models.BooleanField("Is Shared?", default=False)
    ServiceType = models.CharField("Service Type", max_length=30, choices=(('1','Google AdWords'),('2','VoiceStar'),('3','AdCenter')))  #don't ask why this is char's...
    ServiceAccountId = models.CharField('Account ID', max_length=80, blank=False)


    def __unicode__(self):
        lsOwner = self.owner.all()
        if lsOwner:
            return lsOwner[0].AdAccountOwner.Name + " [" + D_SERVICETYPE_CHOICES[self.ServiceType] + "/" + self.ServiceAccountId + "]"
        else:    
            return "--UNOWNED-- [" + D_SERVICETYPE_CHOICES[self.ServiceType] + "/" + self.ServiceAccountId + "]"

    class Meta:
        unique_together=(("ServiceType", "ServiceAccountId"),)


##crazy join idea - makes admin work??
class AdAccountGrouping(models.Model):
    parentaccount = models.ForeignKey(AdAccountOwner, related_name="subaccounts")
    subaccount = models.ForeignKey(AdAccountOwner, related_name="parental", unique=True)

    def __unicode__(self):
        
        return self.parentaccount.Name + " - " + self.subaccount.Name



class AdAccountOwnership(models.Model):
    AdAccountOwner = models.ForeignKey(AdAccountOwner, related_name="adaccounts")
    AdAccount = models.ForeignKey(AdAccount, unique=True, related_name="owner")

    def __unicode__(self):
        
        return self.AdAccountOwner.Name + " - " + D_SERVICETYPE_CHOICES[self.AdAccount.ServiceType] + "/" + self.AdAccount.ServiceAccountId


    #def get_ServiceType_display(self):
    #    return dict([(1,'Google AdWords'),(2,'VoiceStar'),(3,'AdCenter')])[self.ServiceType]

# class ClientAccount(models.Model):
#     Client = models.ForeignKey(LarsClient)
#     Account = models.ForeignKey(Account)
#     #BudgetAllocation = models.DecimalField("Budget Allocated", max_digits=16, decimal_places=2, blank=True, null=True) 
#     #BudgetAllocationPercent = models.DecimalField("Budget Allocated (by %)", max_digits=16, decimal_places=10, blank=True, null=True) 
#     ##how much this client gives to this account... useful in shared situations
#     ## check out https://docs.djangoproject.com/en/dev/ref/contrib/admin/ and list_editable for editing in the change list view of admin

#     def __unicode__(self):
#         sShared = ""
#         #if self.Account.Shared:
#         #    sShared = " (shared)"
#         return self.Client.Name + "/" + self.Account.get_ServiceType_display() + " (" + self.Account.ServiceAccountId + ") - " + self.Account.Name + sShared

#     class Meta:
#         unique_together=(("Client", "Account"),)

# Create your models here.

class AGEmailLog(models.Model):
    Rid = models.CharField('Rid', max_length=255, blank=True)
    StoreNum = models.CharField('StoreNum', max_length=30, blank=False)
    firstname = models.CharField('firstname', max_length=60, blank=True)
    lastname = models.CharField('lastname', max_length=60, blank=True)
    company = models.CharField('company', max_length=255, blank=True)
    address = models.CharField('address', max_length=255, blank=True)
    city = models.CharField('city', max_length=60, blank=True)
    state = models.CharField('state', max_length=30, blank=True)
    zipcode = models.CharField('zipcode', max_length=30, blank=True)
    phone = models.CharField('phone', max_length=50, blank=True)
    email = models.CharField('email', max_length=200, blank=True)
    response = models.CharField('response', max_length=60, blank=True)
    projectname = models.CharField('projectname', max_length=300, blank=True)
    projectduedate = models.CharField('projectduedate', max_length=300, blank=True)
    projectdetails = models.TextField('projectdetails', blank=True)
    offer = models.CharField('offer', max_length=30, blank=True)
    submit = models.CharField('submit', max_length=100, blank=True)
    ServerTime = models.DateField('ServerTime') 
    ServerDateTime = models.DateTimeField('ServerDateTime')  
    misc1 = models.CharField('misc1', max_length=255, blank=True)
    misc2 = models.CharField('misc2', max_length=255, blank=True)
    misc3 = models.CharField('misc3', max_length=255, blank=True)
    misc4 = models.CharField('misc4', max_length=255, blank=True)
    misc5 = models.CharField('misc5', max_length=255, blank=True)






class VoiceStarCallLog(models.Model):
    caller_number = models.CharField('caller_number', max_length=25, blank=True)
    caller_name = models.CharField('caller_name', max_length=75, blank=True)
    call_id = models.CharField('caller_id', max_length=25, unique=True)
    inbound_no = models.CharField('inbound_no', max_length=25)
    inbound_ext = models.CharField('inbound_ext', max_length=25, blank=True)
    keyword = models.CharField('keyword', max_length=255, blank=True)
    forward_no = models.CharField('forward_no', max_length=25, blank=True)
    custom_id = models.CharField('custom_id', max_length=25, blank=True)
    account_id = models.CharField('account_id', max_length=25)
    group_id = models.CharField('group_id', max_length=25)
    campaign_id = models.CharField('campaign_id', max_length=25)
    a_name = models.CharField('a_name', max_length=75)
    g_name = models.CharField('g_name', max_length=50)
    c_name = models.CharField('c_name', max_length=50)
    call_s = models.DateTimeField('call_s')  #CONVERT
    duration = models.IntegerField('duration')  #CONVERT
    answer_offset = models.IntegerField('answer_offset')  #CONVERT
    call_status = models.CharField('call_status', max_length=25)
    disposition = models.CharField('disposition', max_length=25, blank=True)
    rating = models.CharField('rating', max_length=25, blank=True)
    listenedto = models.BooleanField('listenedto')
    dna_class = models.CharField('dna_class', max_length=50, blank=True)
    is_spam = models.BooleanField('is_spam', default=False)
    


class GoogleAccountPerformanceReport(models.Model):
    AccountDescriptiveName = models.CharField('AccountDescriptiveName', max_length=100)
    Date = models.DateField('Date')
    AdNetworkType1 = models.CharField('AdNetworkType1', max_length=50)
    AdNetworkType2 = models.CharField('AdNetworkType2', max_length=50)
    Device = models.CharField('Device', max_length=50)
    ClickType = models.CharField('ClickType', max_length=50)
    AccountCurrencyCode = models.CharField('AccountCurrencyCode', max_length=10)
    AccountId = models.BigIntegerField( 'AccountId')
    AccountTimeZoneId = models.CharField('AccountTimeZoneId', max_length=60)
    Impressions = models.IntegerField('Impressions')
    Clicks = models.IntegerField('Clicks')
    Ctr = models.FloatField('Ctr')
    AverageCpc = models.DecimalField('AverageCpc', decimal_places=2, max_digits=16)
    Cost = models.DecimalField('Cost', decimal_places=2, max_digits=16)
    AveragePosition = models.FloatField('AveragePosition')
    ExternalCustomerId = models.BigIntegerField("Customer Id")
    Conversions = models.BigIntegerField( 'Conversions')
    CostPerConversion =  models.DecimalField('Cost Per Conversion', decimal_places=2, max_digits=16)
    ConversionRate = models.FloatField('Conversion Rate')
    TotalConvValue = models.FloatField( 'Total Conversion Value')
    ViewThroughConversions = models.BigIntegerField( 'View Through Conversions')
    ValuePerConversion = models.FloatField('Value per Conversion')

    class Meta:
        unique_together = (("ExternalCustomerId", "Date", "AdNetworkType1", "AdNetworkType2", "Device", "ClickType"),)

class GoogleCampaignPerformanceReport(models.Model):
## Campaign    Clicks  Impressions CTR  Avg. CPC    Cost   Avg. position   Bookings     Cost / conv. (1-per-click)     Conv. rate (1-per-click)     View-through conv.      Booking value  Booking value / cost     Phone impressions   Phone calls     Phone costs     Total costs 
    ExternalCustomerId = models.BigIntegerField("Customer Id")
    Date = models.DateField('Date')
    AdNetworkType1 = models.CharField('AdNetworkType1', max_length=50)
    AdNetworkType2 = models.CharField('AdNetworkType2', max_length=50)
    #Device = models.CharField('Device', max_length=50)
    ClickType = models.CharField('ClickType', max_length=50)
    AccountDescriptiveName = models.CharField('AccountDescriptiveName', max_length=100)
    AccountCurrencyCode = models.CharField('AccountCurrencyCode', max_length=10)
    AccountId = models.BigIntegerField( 'AccountId')
    AccountTimeZoneId = models.CharField('AccountTimeZoneId', max_length=60)
    CampaignId = models.BigIntegerField("CampaignId")
    CampaignName = models.CharField('Campaign Name', max_length=150)
    CampaignStatus = models.CharField('Campaign Name', max_length=20)
    Impressions = models.BigIntegerField( 'Impressions')
    Clicks = models.IntegerField('Clicks')
    Ctr = models.FloatField('Ctr')
    AverageCpc = models.DecimalField('AverageCpc', decimal_places=2, max_digits=16)
    Cost = models.DecimalField('Cost', decimal_places=2, max_digits=16)
    AveragePosition = models.FloatField('AveragePosition')
    Conversions = models.BigIntegerField( 'Conversions')
    CostPerConversion =  models.DecimalField('Cost Per Conversion', decimal_places=2, max_digits=16)
    ConversionRate = models.FloatField('Conversion Rate')
    TotalConvValue = models.FloatField( 'Total Conversion Value')
    ViewThroughConversions = models.BigIntegerField( 'View Through Conversions')
    ValuePerConversion = models.FloatField('Value per Conversion') #Booking Value?? TotalConvValue? Conversion Value?
    #Booking Value / Cost  (derived, punt for later view)
    #Phone...
    #Phone...
    #Phone...
    #TotalCosts (derived to include phone costs etc)

    class Meta:
        unique_together = (("ExternalCustomerId", "Date", "CampaignId", "AdNetworkType1", "AdNetworkType2", "ClickType"),)



class GoogleKeywordPerformanceReport(models.Model):
## Campaign    Ad group    Keyword Impressions Clicks  CTR  Avg. CPC    Cost    Avg. position  Conv. (1-per-click) Cost / conv. (1-per-click)  Conv. rate (1-per-click)    Total conv. value   View-through conv.
    ExternalCustomerId = models.BigIntegerField("Customer Id")
    Date = models.DateField('Date')
    AdNetworkType1 = models.CharField('AdNetworkType1', max_length=50)
    AdNetworkType2 = models.CharField('AdNetworkType2', max_length=50)
    Device = models.CharField('Device', max_length=50)
    ClickType = models.CharField('ClickType', max_length=50)
    AccountDescriptiveName = models.CharField('AccountDescriptiveName', max_length=100)
    AccountCurrencyCode = models.CharField('AccountCurrencyCode', max_length=10)
    AccountTimeZoneId = models.CharField('AccountTimeZoneId', max_length=60)
    CampaignId = models.BigIntegerField("CampaignId")
    CampaignName = models.CharField('Campaign Name', max_length=150)
    CampaignStatus = models.CharField('Campaign Name', max_length=20)
    AdGroupId = models.BigIntegerField("AdGroupId")
    AdGroupName = models.CharField('AdGroup Name', max_length=150)
    AdGroupStatus = models.CharField('AdGroup Name', max_length=20)
    KeywordId = models.BigIntegerField("Keyword Id")#NOTE: Field name in APU is just Id"
    KeywordText = models.CharField("Keyword Text", max_length=200)
    KeywordMatchType = models.CharField('Keyword Match Type', max_length=20)
    Impressions = models.BigIntegerField( 'Impressions')
    Clicks = models.IntegerField('Clicks')
    Ctr = models.FloatField('Ctr')
    AverageCpc = models.DecimalField('AverageCpc', decimal_places=2, max_digits=16)
    Cost = models.DecimalField('Cost', decimal_places=2, max_digits=16)
    AveragePosition = models.FloatField('AveragePosition')
    Conversions = models.BigIntegerField( 'Conversions')
    CostPerConversion =  models.DecimalField('Cost Per Conversion', decimal_places=2, max_digits=16)
    ConversionRate = models.FloatField('Conversion Rate')
    TotalConvValue = models.FloatField( 'Total Conversion Value')
    ViewThroughConversions = models.BigIntegerField( 'View Through Conversions')
    ValuePerConversion = models.FloatField('Value per Conversion')

    class Meta:
        unique_together = (("ExternalCustomerId", "Date", "AdGroupId", "KeywordId", "AdNetworkType1", "AdNetworkType2", "Device", "ClickType"),)


class GoogleGeoPerformanceReport(models.Model):
# Country/Territory   Region  City    Impressions Clicks  CTR Avg. CPC    Cost    Avg. position   Conv. (1-per-click) Cost / conv. (1-per-click)  Conv. rate (1-per-click)    Total conv. value   View-through conv.
    ExternalCustomerId = models.BigIntegerField("Customer Id")
    Date = models.DateField('Date')
    AdNetworkType1 = models.CharField('AdNetworkType1', max_length=50)
    AdNetworkType2 = models.CharField('AdNetworkType2', max_length=50)
    Device = models.CharField('Device', max_length=50)
    #ClickType = models.CharField('ClickType', max_length=50) #not available in Geo as of 2/2013
    AccountDescriptiveName = models.CharField('AccountDescriptiveName', max_length=100)
    AccountCurrencyCode = models.CharField('AccountCurrencyCode', max_length=10)
    AccountTimeZoneId = models.CharField('AccountTimeZoneId', max_length=60)
    CampaignId = models.BigIntegerField("CampaignId")
    CampaignName = models.CharField('Campaign Name', max_length=150)
    CampaignStatus = models.CharField('Campaign Name', max_length=20)
    AdGroupId = models.BigIntegerField("AdGroupId")
    AdGroupName = models.CharField('AdGroup Name', max_length=150)
    AdGroupStatus = models.CharField('AdGroup Name', max_length=20)
    LocationType = models.CharField('Location Type', max_length=40)
    CountryCriteriaId = models.CharField('Metro Criteria Id', max_length=150)
    RegionCriteriaId = models.CharField('Metro Criteria Id', max_length=150)
    MetroCriteriaId = models.CharField('Metro Criteria Id', max_length=150)
    CityCriteriaId = models.CharField('Metro Criteria Id', max_length=150)
    Impressions = models.BigIntegerField( 'Impressions')
    Clicks = models.IntegerField('Clicks')
    Ctr = models.FloatField('Ctr')
    AverageCpc = models.DecimalField('AverageCpc', decimal_places=2, max_digits=16)
    Cost = models.DecimalField('Cost', decimal_places=2, max_digits=16)
    AveragePosition = models.FloatField('AveragePosition')
    Conversions = models.BigIntegerField( 'Conversions')
    CostPerConversion =  models.DecimalField('Cost Per Conversion', decimal_places=2, max_digits=16)
    ConversionRate = models.FloatField('Conversion Rate')
    TotalConvValue = models.FloatField( 'Total Conversion Value')
    ViewThroughConversions = models.BigIntegerField( 'View Through Conversions')
    ValuePerConversion = models.FloatField('Value per Conversion')


    class Meta:
        unique_together = (("ExternalCustomerId", "Date", "AdGroupId", "LocationType", "CountryCriteriaId", "RegionCriteriaId", "MetroCriteriaId", "CityCriteriaId", "AdNetworkType1", "AdNetworkType2", "Device"),)













