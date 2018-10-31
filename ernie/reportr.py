#-*- coding:utf-8 -*-
import sys, os, logging, collections, time, operator, pytz, datetime
PROJECT_ROOT = os.path.abspath( 
    os.path.dirname(__file__) + "../" 
)
sys.path = [PROJECT_ROOT] + sys.path   
from django.core.management import setup_environ
from lars import settings
setup_environ(settings)

from django import db
import httplib, httplib2, time, csv, datetime
from dateutil import parser
from django.db import transaction
#from apiclient.discovery import build


# from adspygoogle.adwords import AdWordsClient #import AdWordsClient
# from adspygoogle.adwords.AdWordsErrors import AdWordsReportError, AdWordsError
# from adspygoogle.common.Errors import ValidationError
from googleads import adwords
from googleads.errors import AdWordsReportError, GoogleAdsError


from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError, SignedJwtAssertionCredentials

from main import models
import eventlet
from eventlet import pools
#eventlet.monkey_patch()
# import httplib2, pymongo
# httplib2 = eventlet.import_patched('httplib2')

#AdWordsClient = eventlet.import_patched('adspygoogle.adwords.AdWordsClient')
AdWordsClient = eventlet.import_patched('googleads.adwords')

#### Notes:
# rows  table
# 5,000         account
# 67,000        campaign
# 1,050,000     keyword
# 12,000,000+   geo



loggr = logging.getLogger("")
loggr.setLevel(logging.INFO)

#S_API_VERSION = "v201309"
#S_API_VERSION = "v201402"
#S_API_VERSION = "v201406"
#S_API_VERSION = "v201409"
#S_API_VERSION = "v201502"
#S_API_VERSION = "v201506"
#S_API_VERSION = "v201509"
#S_API_VERSION = "v201603"
S_API_VERSION = "v201609"

_CHUNK_SIZE = 16 * 1024

CALL_SPAM_SEC_DURATION = 20
CALL_SPAM_OK_START_TIME = datetime.time(7,0,0)
CALL_SPAM_OK_END_TIME = datetime.time(18,30,0)
CALL_SPAM_CALL_STATUS_NOFORWARDS = u"NOFORWARDS"

F_MARKUP = 1.26
F_MIN_AMOUNT = 100.00


# SCOPES = ["https://www.googleapis.com/auth/drive"]

# f = file('/home/ubuntu/.ssh/7004da0bd9962cdea75e3cea160ad6169b2c3187-privatekey.p12', 'rb')
# key = f.read()
# f.close()
# # Visit https://code.google.com/apis/console to generate your client_id,
# # client_secret and to register your redirect_uri.
# # See the oauth2client wiki for more information on performing the OAuth2 flow:
# # http://code.google.com/p/google-api-python-client/wiki/OAuth2
# oauth2_client_id = '961209305009.apps.googleusercontent.com'
# oauth2_client_secret = 'pDtTzkVzgBuWM9I2HJd9uPJ_'
# oauth2_client_email = '961209305009@developer.gserviceaccount.com'

# credentials = SignedJwtAssertionCredentials(oauth2_client_email, key,scope=" ".join(SCOPES))
#         # ,                     
#         # scope=['https://www.googleapis.com/auth/calendar',                      
#         #        'https://www.googleapis.com/auth/calendar.readonly'])            
# http = httplib2.Http()              
# httplib2.debuglevel = True                                    
# http = credentials.authorize(http) 

#service = build(serviceName='drive', version='v2', http=http)

#print service.files().list().execute()


# service = build(serviceName='calendar', version='v3', http=http,       
#          developerKey='XcddfRgtyt676grggtT') 


sandbox_email = 'larsmarketing@arborheights.net'
client_customer_id = '433-908-0283'


DO_NOT_IMPORT = [

8310256288, #ClassifiedAds.com jwilson@bluemoonventures.com
9663107432,#PF peoplenames@peoplefinders.com
9655991032, #PR360 WebKrux,pubrec360@gmail.com
7284571322 #MWM mwm@larsmarketing.com

]


ADNETWORKTYPE1_SEARCH_NETWORK_KEY = u'Search Network'
ADNETWORKTYPE1_DISPLAY_NETWORK_KEY = u'Display Network'

ADNETWORKTYPE1_LABELS = {
    ADNETWORKTYPE1_SEARCH_NETWORK_KEY: "Total - Search",
    ADNETWORKTYPE1_DISPLAY_NETWORK_KEY: "Total - Display Network",
}

CURRENCYCODE_TO_SYMBOL = {
  "USD":"$",
  "CAD":"C$",
  "BRL":"R$"
}

CLICKTYPES_TO_INCLUDE = [
'Phone calls',
'Headline'  
]


# # We're using the oauth2client library:
# # http://code.google.com/p/google-api-python-client/downloads/list
# flow = OAuth2WebServerFlow(
#     client_id=oauth2_client_id,
#     client_secret=oauth2_client_secret,
#     # Scope is the server address with '/api/adwords' appended.
#     scope='https://adwords-sandbox.google.com/api/adwords',
#     user_agent='oauth2 code example')

# # Get the authorization URL to direct the user to.
# authorize_url = flow.step1_get_authorize_url(redirect_uri='oob')

# credential = None
# try:
#   credential = flow.step2_exchange(code)
# except FlowExchangeError, e:
#   sys.exit('Authentication has failed: %s' % e)

#  # Create the AdWordsUser and set the OAuth2 credentials.
# client = AdWordsClient(headers={
#     'developerToken': '%s++USD' % sandbox_email,
#     'clientCustomerId': client_customer_id,
#     'userAgent': 'OAuth2 Example',
#     'oauth2credentials': credentials
# })

# # # OAuth2 credentials objects can be reused
# credentials = client.oauth2credentials
# # print 'OAuth2 authorization successful!'


#########

# OAuth2 credential objects can be refreshed via credentials.refresh() - the
# access token expires after 1 hour.
#credentials.refresh(httplib2.Http())

# Note: you could simply set the credentials as below and skip the previous
# steps once access has been granted.
#client.oauth2credentials = credentials











# client = AdWordsClient(headers={'authToken': ' ',
#                                     'userAgent': ' ',
#                                     'developerToken': ' '})

def getClient():
    # client = AdWordsClient.AdWordsClient(path='~/', headers={
    #     'clientCustomerId': '433-908-0283', #Lars MCC

    #     #'clientCustomerId': '990-671-7951', #SANDBOX ACCT
    #     #'clientCustomerId':'450-614-3003',
    #     #'clientCustomerId':'9663107432',
    #  'developerToken': 'KuxisPFnqHFfkJetsOyMGQ',
    #  'email': 'larsmarketing@arborheights.net',
    #  'password': 'babal000',
    #  'userAgent': 'Lars',
    #  'debug': 'n',
    #  'home': '/home/ubuntu',
    #  'log_home': '/home/ubuntu/logs',
    #  'request_log': 'n',
    #  'xml_log': 'n',
    #  'xml_parser': '1'})

    # client = AdWordsClient.AdWordsClient()
    # if not client.oauth2credentials.access_token:
    #     creds = client.oauth2credentials
    #     creds.refresh(httplib2.Http())
    #     client.oauth2credentials = creds
    # return client

    client = adwords.AdWordsClient.LoadFromStorage('/home/ubuntu/googleads.yaml')
    return client


#client = AdWordsClient(path='~/')
# #client.use_mcc = True
#dlr = client.GetReportDownloader()


## WORKS!!!
def DisplayAccountTree(account, link, accounts, links, depth=0):
    """Displays an account tree.

    Args:
    account: dict The account to display.
    link: dict The link used to reach this account.
    accounts: dict Map from customerId to account.
    links: dict Map from customerId to child links.
    depth: int Depth of the current account in the tree.
    """
    prefix = '-' * depth * 2
    print '%s%s, %s, %s' % (prefix, account.get('login', ''), account['customerId'],
                          account['name'])
    if account['customerId'] in links:
        for child_link in links[account['customerId']]:
            child_account = accounts[child_link['clientCustomerId']]
            DisplayAccountTree(child_account, child_link, accounts, links, depth + 1)



def _convertSudsToOldStyle(o):
    dO = dict(o)
    if dO.has_key('customerId'):
        dO['customerId'] = unicode(dO['customerId'])
    if dO.has_key('name'):
        dO['name'] = unicode(dO['name'])
    if dO.has_key('clientCustomerId'):
        dO['clientCustomerId'] = unicode(dO['clientCustomerId'])
    if dO.has_key('managerCustomerId'):
        dO['managerCustomerId'] = unicode(dO['managerCustomerId'])
    return dO



def getAccounts(showTree=False):
    #Initialize appropriate service.
    client = getClient()
    managed_customer_service = client.GetService(
      'ManagedCustomerService', version=S_API_VERSION )

    # Construct selector to get all accounts.
    selector = {
      'fields': ['CustomerId', 'Name']
    }
    # Get serviced account graph.
    graph = managed_customer_service.get(selector)
    if 'entries' in graph and graph['entries']:
        # Create map from customerId to parent and child links.
        child_links = {}
        parent_links = {}
        if 'links' in graph:
            for link in graph['links']:
                link = _convertSudsToOldStyle(link)
                if link['managerCustomerId'] not in child_links:
                    child_links[link['managerCustomerId']] = []
                child_links[link['managerCustomerId']].append(link)
                if link['clientCustomerId'] not in parent_links:
                    parent_links[link['clientCustomerId']] = []
                parent_links[link['clientCustomerId']].append(link)
        # Create map from customerID to account and find root account.
        accounts = {}
        root_account = None
        for account in graph['entries']:
            account = _convertSudsToOldStyle(account)
            accounts[account['customerId']] = account
            if account['customerId'] not in parent_links:
                root_account = account
        # Display account tree.
        if root_account:
            if showTree:
                print 'CustomerId, Name'
                DisplayAccountTree(root_account, None, accounts, child_links, 0)
        else:
            print 'Unable to determine a root account'
    else:
        print 'No serviced accounts were found'

  

    return root_account, accounts, child_links

def getAccountsByParent(sParentId, includeParent=False):
    d = models.mongodb.reports.find_one({"customerId":sParentId})
    subset = d['subIds']
    if includeParent:
        subset.append(sParentId) 
    return sorted(subset)

def getEndNodeCustomerIds(masterId=None):
    a,b,c = getAccounts()
    sAllIds = set(b.keys())
    sMgrIds = set(c.keys())
    sEndNodeIds = sAllIds.difference(sMgrIds)

    ## now prune
    for iPruneId in DO_NOT_IMPORT:
        if c.has_key(unicode(iPruneId)):
            sEndNodeIds = sEndNodeIds.difference([d['clientCustomerId'] for d in c[unicode(iPruneId)]])
        else:
            if unicode(iPruneId) in sEndNodeIds:
                sEndNodeIds.remove(unicode(iPruneId))


    if masterId:
        sSubIds = set([x['clientCustomerId'] for x in c[masterId]])

        sResult = sSubIds.intersection(sEndNodeIds)
    else:
        sResult = sEndNodeIds

    lsCustIds = list(sResult) #[:10]

    




    return lsCustIds


def syncAccountCache():
    a,b,c = getAccounts()

    ##currently looks safe to assume all accounts in b are in the hierarchy of c somewhere
    # sInHierarchy = set()
    # for k,v in c.iteritems():
    #     sInHierarchy.add(k)
    #     sInHierarchy.update([x['clientCustomerId'] for x in c[k]])
    x = models.mongodb.reports.remove()

    for k, d in b.iteritems():
        d = dict(d)
        d['customerId'] = unicode(d['customerId'])
        d['subIds'] = []
        if k in c.keys():
            d['subIds'] += [unicode(x['clientCustomerId']) for x in c[k]]
        models.mongodb.reports.update({"customerId":d['customerId']}, d, upsert=True)


def syncMissingAccountsDB():
    dtNow = datetime.datetime.now(pytz.UTC)
    lsGoog = models.mongodb.reports.find()
    #lsMasters = models.MasterAccount.objects.all()

    sGids = set([x.ServiceAccountId for x in models.AdAccount.objects.filter(ServiceType__exact=1)])
    sAllGids = set([x['customerId'] for x in lsGoog])

    sNew = sAllGids.difference(sGids)
    sRemoved = sGids.difference(sAllGids)
    i = 0

    #logging.warning(sRemoved)
    #logging.warning(sNew)

    lsNew = models.mongodb.reports.find({'customerId':{'$in':list(sNew)}})
    for dNew in lsNew:
        print "CREATE", "GOOG", dNew['name'], dNew['customerId']
        #ac = models.Account(Name=dNew['name'], Active=True, ServiceType='1', ServiceAccountId=dNew['customerId'], Group_id=297)
        #ac.save()
        aac = models.AdAccount(Name=dNew['name'], Active=True, ServiceType='1', ServiceAccountId=dNew['customerId'])
        aac.save()
        i += 1
        
    dAllVSids = {}
    sVSids = set([x.ServiceAccountId for x in models.AdAccount.objects.filter(ServiceType__exact=2)])
    for x in models.VoiceStarCallLog.objects.filter(call_s__gte=dtNow-datetime.timedelta(days=90)): 
        if not dAllVSids.has_key(x.account_id):
            dAllVSids[x.account_id] = {"name":x.a_name}  

    
    sAllVSids = set(dAllVSids.iterkeys())
    sNewVS = sAllVSids.difference(sVSids)
    sRemovedVS = sVSids.difference(sAllVSids)

    for sNewId in sNewVS:
        print "CREATE", "VS", dAllVSids[sNewId]['name'], sNewId
        #ac = models.Account(Name=dAllVSids[sNewId]['name'], Active=True, ServiceType='2', ServiceAccountId=sNewId, Group_id=297)
        #ac.save()
        aac = models.AdAccount(Name=dAllVSids[sNewId]['name'], Active=True, ServiceType='2', ServiceAccountId=sNewId)
        aac.save()

        i += 1

    print i


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days+1)):
        yield start_date + datetime.timedelta(n)


def getStrDates(dtStart, dtEnd):
    dates = []
    for single_date in daterange(dtStart, dtEnd):
        dates.append(single_date.strftime("%Y%m%d"))

    dates = sorted(dates)
    return dates



# campaign_service = client.GetCampaignService(
#       'https://adwords.google.com', 'v201209')

# PAGE_SIZE = 25
# offset = 0
# selector = {
#       'fields': ['Id', 'Name', 'Status'],
#       'paging': {
#           'startIndex': str(offset),
#           'numberResults': str(PAGE_SIZE)
#       }
#   }

# more_pages = True
# while more_pages:
#   page = campaign_service.Get(selector)[0]

#   # Display results.
#   if 'entries' in page:
#       for campaign in page['entries']:
#           print ('Campaign with id \'%s\', name \'%s\', and status \'%s\' was '
#               'found.' % (campaign['id'], campaign['name'],
#                          campaign['status']))
#   else:
#       print 'No campaigns were found.'
#   offset += PAGE_SIZE
#   selector['paging']['startIndex'] = str(offset)
#   more_pages = offset < int(page['totalNumEntries'])
#   time.sleep(1)

# print
# print ('Usage: %s units, %s operations' % (client.GetUnits(),
#                                          client.GetOperations()))


# TODAY   보고서가 오늘에 대해서만 생성됩니다.
# YESTERDAY   보고서가 어제에 대해서만 생성됩니다.
# LAST_7_DAYS 보고서가 오늘을 제외한 지난 7일에 대해 생성됩니다.
# THIS_WEEK_SUN_TODAY 지난 일요일부터 오늘까지의 기간에 대해 보고서가 생성됩니다.
# THIS_WEEK_MON_TODAY 지난 월요일부터 오늘까지의 기간에 대해 보고서가 생성됩니다.
# LAST_WEEK   보고서가 지난 월요일부터 계산한 7일 기간에 대해 생성됩니다.
# LAST_14_DAYS    보고서가 오늘을 제외한 지난 14일에 대해 생성됩니다.
# LAST_30_DAYS    보고서가 오늘을 제외한 지난 30일에 대해 생성됩니다.
# LAST_BUSINESS_WEEK  보고서가 지난 월요일부터 계산한 5일 영업주에 대해 생성됩니다.
# LAST_WEEK_SUN_SAT   보고서가 지난 일요일부터 계산한 7일 기간에 대해 생성됩니다.
# THIS_MONTH  보고서가 이번 달에 포함된 모든 날에 대해 생성됩니다.
# LAST_MONTH  보고서가 지난 달에 포함된 모든 날에 대해 생성됩니다.
# ALL_TIME    보고서가 사용 가능한 모든 시간 범위에 대해 생성됩니다.
# CUSTOM_DATE

REPORT_DL_PATH = '/home/ubuntu/dlreports/'
REPORT_DUMP_PATH = '/home/ubuntu/lars/static/reportExport/'

dReportSpecs = {
    'account':{
        'file_prefix':'googAcctPerf_',
        'report_spec':{                     
          #'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
          'reportName':'ACCOUNT_PERFORMANCE_REPORT',
          #'dateRangeType': 'LAST_7_DAYS',
          #'dateRangeType': 'LAST_30_DAYS',
          'dateRangeType': 'CUSTOM_DATE',
          
          'reportType': 'ACCOUNT_PERFORMANCE_REPORT',
          'downloadFormat': 'CSV',
          'selector': {
              #'fields': ['AccountDescriptiveName', 'Date', 'AccountCurrencyCode', 'ExternalCustomerId','AccountTimeZoneId',
              #              'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition','AdNetworkType1', 'AdNetworkType2', 'Device', 'ClickType','ConvertedClicks','CostPerConvertedClick', 'ClickConversionRate', 'ConversionValue', 'ViewThroughConversions','ValuePerConvertedClick'],
              
              # 11/2016 - Google changed schema from ConvertedClicks to Conversions
              'fields': ['AccountDescriptiveName', 'Date', 'AccountCurrencyCode', 'ExternalCustomerId','AccountTimeZoneId',
                            'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition','AdNetworkType1', 'AdNetworkType2', 'Device', 'ClickType','Conversions','CostPerConversion', 'ConversionRate', 'ConversionValue', 'ViewThroughConversions','ValuePerConversion'],




              ## entered below... 'dateRange':{'min':sDate, 'max':sDate} #['20130101', '20130121']
          }
        }
    },
    'campaign':{
        'file_prefix':'googCampPerf_',
        'report_spec': {                     
          #'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
          'reportName':'CAMPAIGN_PERFORMANCE_REPORT',
          'dateRangeType': 'CUSTOM_DATE',
          #'dateRangeType': 'LAST_30_DAYS',
          'reportType': 'CAMPAIGN_PERFORMANCE_REPORT',
          'downloadFormat': 'CSV',
          'selector': {
              'fields': ['ExternalCustomerId', 'Date', 'AccountDescriptiveName', 'AccountCurrencyCode', 'AccountTimeZoneId', 
                    'CampaignId', 'CampaignName', 'CampaignStatus', 'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition',
                    #'ConvertedClicks','CostPerConvertedClick', 'ClickConversionRate', 'ConversionValue', 'ViewThroughConversions','ValuePerConvertedClick',
                    #'AdNetworkType1', 'AdNetworkType2', 'ClickType'],

                    # 11/2016 - Google changed schema from ConvertedClicks to Conversions
                    'Conversions','CostPerConversion', 'ConversionRate', 'ConversionValue', 'ViewThroughConversions','ValuePerConversion',
                    'AdNetworkType1', 'AdNetworkType2', 'ClickType'],  
                    #cant do 'Device' and "numOfflineImpressions" at same time
                    #cant do since beta - 'NumOfflineImpressions','NumOfflineInteractions','OfflineInteractionCost','OfflineInteractionRate', 
              ##'dateRange':{'min':sDate, 'max':sDate} 
          }
        }

    },
    'keyword':{
        'file_prefix':'googKeywPerf_',
        'report_spec':{                     
          #'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
          'reportName':'KEYWORDS_PERFORMANCE_REPORT',
          'dateRangeType': 'CUSTOM_DATE',
          #'dateRangeType': 'LAST_30_DAYS',
          'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
          'downloadFormat': 'CSV',
          'selector': {
              'fields': ['ExternalCustomerId', 'Date', 'AccountDescriptiveName', 'AccountCurrencyCode', 'AccountTimeZoneId', 
                    'CampaignId', 'CampaignName', 'CampaignStatus', 'AdGroupId', 'AdGroupName', 'AdGroupStatus', 'Id', 
                    'Criteria', 'KeywordMatchType', 'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition',
                    #'ConvertedClicks', 'CostPerConvertedClick', 'ClickConversionRate', 'ConversionValue', 'ViewThroughConversions','ValuePerConvertedClick',
                    
                    # 11/2016 - Google changed schema from ConvertedClicks to Conversions
                    'Conversions','CostPerConversion', 'ConversionRate', 'ConversionValue', 'ViewThroughConversions','ValuePerConversion',
                    
                    'AdNetworkType1', 'AdNetworkType2', 'Device', 'ClickType'],
              




              ##'dateRange':{'min':sDate, 'max':sDate} 
          }
        }

    },
    'geo':{
        'file_prefix':'googGeoPerf_',
        'report_spec':{                     
          #'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
          'reportName':'GEO_PERFORMANCE_REPORT',
          'dateRangeType': 'CUSTOM_DATE',
          #'dateRangeType': 'LAST_14_DAYS',
          #'dateRangeType':'CUSTOM_DATE',
          'reportType': 'GEO_PERFORMANCE_REPORT',
          'downloadFormat': 'CSV',
          'selector': {
              'fields': ['ExternalCustomerId', 'Date', 'AccountDescriptiveName', 'AccountCurrencyCode', 'AccountTimeZoneId', 
                    'CampaignId', 'CampaignName', 'CampaignStatus', 'AdGroupId', 'AdGroupName', 'AdGroupStatus', 'LocationType', 
                    'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId', 'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition',
                    #'ConvertedClicks', 'CostPerConvertedClick', 'ClickConversionRate', 'ConversionValue', 'ViewThroughConversions','ValuePerConvertedClick',

                    # 11/2016 - Google changed schema from ConvertedClicks to Conversions
                    'Conversions','CostPerConversion', 'ConversionRate', 'ConversionValue', 'ViewThroughConversions','ValuePerConversion',
                    
                    'AdNetworkType1', 'AdNetworkType2', 'Device'],  #ClickType not available
               ##'dateRange':{'min':sDate, 'max':sDate} 
          }
        }

    },
    ##not needed right now
    # 'call':{
    #     'file_prefix':'googCallPerf_',
    #     'report_spec':{                     
    #       #'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
    #       'reportName':'CALL_PERFORMANCE_REPORT',
    #       'dateRangeType': 'CUSTOM_DATE',
    #       #'dateRangeType': 'LAST_14_DAYS',
    #       #'dateRangeType':'CUSTOM_DATE',
    #       'reportType': 'CALL_PERFORMANCE_REPORT',
    #       'downloadFormat': 'CSV',
    #       'selector': {
    #           'fields': ['ExternalCustomerId', 'Date', 'AccountDescriptiveName', 'AccountCurrencyCode', 'AccountTimeZoneId', 
    #                 'CampaignId', 'CampaignName', 'CampaignStatus', 'AdGroupId', 'AdGroupName', 'AdGroupStatus', 'LocationType', 
    #                 'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId', 'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition','ConvertedClicks',
    #                 'CostPerConvertedClick', 'ClickConversionRate', 'ConversionValue', 'ViewThroughConversions','ValuePerConvertedClick','AdNetworkType1', 'Device', 'ClickType'],
    #            ##'dateRange':{'min':sDate, 'max':sDate} 
    #       },
    #       # Enable to get rows with zero impressions.
    #       'includeZeroImpressions': 'false'
    #     }

    # }

}



# def _getDlr(sCustId):
#   client = getClient()
#   client.SetClientCustomerId(sCustId)
#   return client.GetReportDownloader('https://adwords.google.com', 'v201209')

import requests
def dlVoiceStarReports(lsSDates, force=False):
    directory = REPORT_DL_PATH + "/VoiceStar"
    if not os.path.exists(directory):
        os.makedirs(directory)

    s = requests.session()
    res = s.post('http://calls.larsmarketing.com/login-1', data={'email':'larsmarketing@arborheights.net','passwd':'lars1234'})
    for sDate in lsSDates:

        filepath = directory + "/" + sDate + "_voicestar.csv"
        if force or not os.path.exists(filepath):

            sFormattedDate = "%s-%s-%s" % (sDate[:4],sDate[4:6],sDate[6:])
            print sFormattedDate
            res = s.get('http://calls.larsmarketing.com/api/rest/client/calls/log?output=csv;per_page=0;filter=;acc=CA6ph0odn9g93wDu;status=;start=%s;end=%s;tag=;category=;duration=;listened=;unique=' % (sFormattedDate,sFormattedDate))
            fDL = open(filepath, 'w')
            fDL.write(res.text.encode('utf-8'))
            fDL.close()




def dlReports(sReportType, lsCustIds, lsSDates, force=False, diroverride=None):
    dlrpool = pools.Pool(create=lambda: getClient(), max_size=10)

    if sReportType not in dReportSpecs.keys():
        raise Exception("Bad Report Type")
    
    

    for sCustId in lsCustIds:
        print "Downloading custid", sCustId
        logging.info("Downloading custid %s" % sCustId)
        
        if diroverride:
            directory = diroverride + str(sCustId)
        else:
            directory = REPORT_DL_PATH + str(sCustId)

        if not os.path.exists(directory):
            os.makedirs(directory)

        
        
        #dlr = None


        with dlrpool.item() as client:


            client.SetClientCustomerId(sCustId)
            dlr = client.GetReportDownloader(server='https://adwords.google.com', version=S_API_VERSION )
            for sDate in lsSDates:
                
                filepath = directory + "/" + dReportSpecs[sReportType]['file_prefix'] + sCustId + '_' + sDate + '.csv'
                if force or not os.path.exists(filepath):
                    dReportSpecs[sReportType]['report_spec']['selector']['dateRange'] = {'min':sDate, 'max':sDate}

                    iTries = 0
                    completed = None
                    while not completed and iTries < 3:
                        iTries += 1
                        # if not dlr:
                        #     client = getClient()
                        #     client.SetClientCustomerId(sCustId)
                        #     dlr = client.GetReportDownloader('https://adwords.google.com', S_API_VERSION )

                        try:


                            #logging.warning([dReportSpecs[sReportType]['report_spec'], filepath])
                            #completed_file_path = dlr.DownloadReport(dReportSpecs[sReportType]['report_spec'], file_path=filepath)


                            #report_data = StringIO.StringIO()
                            report_data = open(filepath, 'wb')
                            stream_data = dlr.DownloadReportAsStream(dReportSpecs[sReportType]['report_spec'])

                            try:
                              while True:
                                chunk = stream_data.read(_CHUNK_SIZE)
                                if not chunk: break
                                report_data.write(chunk.decode() if sys.version_info[0] == 3
                                                  and getattr(report_data, 'mode', 'w') == 'w' else chunk)
                              
                            finally:
                              report_data.close()
                              stream_data.close()
                              completed = True




                        except (AdWordsReportError, GoogleAdsError), e:
                            #ALSO HAS e.trigger and e.field_path
                            logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                            
                            if hasattr(e, 'http_code') and e.http_code == '400' and e.type == 'SizeLimitError.RESPONSE_SIZE_LIMIT_EXCEEDED':
                                ## break it up
                                raise

                                
                            elif hasattr(e, 'http_code') and e.http_code == '500' and e.type == 'ReportDownloadError.INTERNAL_SERVER_ERROR':
                                time.sleep(iTries * 2)
                                continue



                            raise

                        except httplib.IncompleteRead, e:
                            logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                            ## retry
                            time.sleep(iTries * 2)
                            continue

                    if iTries >= 3:
                      raise Exception("Too many errors, out of tries")



                

def dlAllReports(lsCustIds, lsSDates, force=False):
    ## google
    for sReportType in dReportSpecs.keys():
        dlReports(sReportType, lsCustIds, lsSDates, force=force)

    ## voicestar
    loadVoiceStarCSV(lsSDates, forceupdate=True)

import filecmp


def sizecompare(f1, f2):
    if not os.path.getsize(f1) == os.path.getsize(f2):
        return False
    else:
        return True



def verifyDlReport(sCustId, sType, lsSDates=[], andFix=False):
    lsLogs = []
    for sDate in lsSDates:
        file_path = REPORT_DL_PATH + sCustId + "/" + dReportSpecs[sType]['file_prefix'] + sCustId + '_' + sDate + '.csv'
        try:
            p = os.stat(file_path)
        except:
            continue  #original file doesn't exist, no need to verify... may be a new client

        verify_directory = REPORT_DL_PATH + "tmpVerify/" 
        if not os.path.exists(verify_directory):
            os.makedirs(verify_directory)

        verify_file_path = verify_directory + sCustId + "/" + dReportSpecs[sType]['file_prefix'] + sCustId + '_' + sDate + '.csv'
        
        iTries = 0
        bDwnd = False            
        while not bDwnd and iTries < 3:
            try:
                dlReports(sType, [sCustId], [sDate], force=True, diroverride=verify_directory)
                bDwnd = True
            except:
                iTries += 1

        if not bDwnd:
            raise Exception("Couldn't dl report after 3 tries")

        lsVerifyLog = [sCustId, sType, sDate,  sizecompare(verify_file_path, file_path), filecmp.cmp(verify_file_path, file_path)]

        if andFix:
            if not lsVerifyLog[3] or not lsVerifyLog[4]:
                print lsVerifyLog

                #TODO - copy latest csv to real path, then modify loadCSV to not re-download

                loadCSV(lsVerifyLog[0], lsVerifyLog[1], [lsVerifyLog[2]], forceupdate=True)

        lsLogs.append(lsVerifyLog)
        #if not sizecompare(verify_file_path, file_path):
        #    logging.warning(["\n\n\n\n\n\n\n\n\nCHANGED", sCustId, sType, sDate, "\n\n\n\n\n\n\n"])




    return lsLogs

def verifyAndRefresh():
  pass #TODO

def verifyAllReports(lsCustIds, lsSDates, andFix=False, logFalseOnly=True):
    lsReportTypesForNow = ["campaign"] #"account", 
    #for sReportType in dReportSpecs.keys():
    lsLogs = []
    for sCustId in lsCustIds:
        lsTheseLogs = []
        for sReportType in lsReportTypesForNow:
        
            lsTheseLogs += verifyDlReport(sCustId, sReportType, lsSDates=lsSDates, andFix=andFix)


        

        lsLogs += lsTheseLogs


    if logFalseOnly:
        lsLogs = [lsLog for lsLog in lsLogs if not lsLog[3] or not lsLog[4]]
            

    return lsLogs


from decimal import Decimal
import dateutil.parser
import pytz
etz = pytz.timezone("US/Eastern")
ptz = pytz.timezone("US/Pacific")

def toUTC(dt, fromTZ):
    """
    takes naive, tz unaware datetime and converts to UTC, accounting for dst as well
    """
    return fromTZ.normalize(fromTZ.localize(dt)).astimezone(pytz.utc)

from ernie import emailIngestr
import xlrd

#@transaction.commit_manually
def loadAGEmailLog(lsSDates=[], autofetch=True, forceupdate=False):

    iNewRecords = 0
    emailIngestr.dlAGEmailLog(lsSDates)  #note, only dls from oldest date to current

    dtOldest = dateutil.parser.parse('20130701')
    for sDate in lsSDates:

        dtDate = dateutil.parser.parse(sDate)
        print dtDate, dtOldest
        if dtDate >= dtOldest and dtDate.date() < datetime.datetime.now(ptz).date():  # DO NOT GO BACK BEYOND 7/1/2013

            existingEmailIds = models.AGEmailLog.objects.filter(ServerTime__exact=dtDate.date()).values_list("Rid", "StoreNum", "phone", "ServerDateTime")
            dExisting = collections.defaultdict(dict)

            
            sDTRange = set()

            for vals in existingEmailIds:
                dExisting[sDate][u"_".join([unicode(x) for x in vals])] = True

            print dExisting

            file_path = REPORT_DL_PATH + "AGEmailedReports/" + sDate + "_AGEmailed.xls"
            print file_path

            try:
                p = os.stat(file_path)
                bFileExists = True
            except OSError:
                bFileExists = False

            if bFileExists:
                wb = xlrd.open_workbook(file_path)
                sh = wb.sheet_by_name('Query')
                #with open(file_path, 'rb') as csvfile:
                #    csvreader = csv.reader(csvfile)
                    #print '1'
                latestIds = set()
                for i in xrange(sh.nrows):
                    row = sh.row_values(i)
                #for i, row in enumerate(csvreader):
                    
                    if i % 1000 == 0: print i, "ag email log"


                    dt = parser.parse(row[17], fuzzy=True).replace(tzinfo=ptz)

                    #print ', '.join(row)
                    
                    if len(row) != 0 and i != 0:
                        sPseudoId = u"_".join([unicode(x) for x in [row[0].strip(), row[1].strip(), row[9].strip(), dt.astimezone(pytz.UTC)]])
                        latestIds.add(sPseudoId)
                        #print sPseudoId
                        #print row
                        o = None
                        if sPseudoId not in dExisting[sDate].keys():
                            #print parser.parse(row[1]).date(), existingDates, sCustId
                            #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                            o = models.AGEmailLog()

                        #### won't work currently, need unique key
                        ##elif forceupdate:
                        ##    o, bCreated = models.AGEmailLog.objects.get_or_create(call_id__exact=row[2])

                        #print parser.parse(row[1]).date(), existingDates, sCustId
                        if o:
                            #print parser.parse(row[1]).date(), existingDates, sCustId
                            #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                            
                            o.Rid = row[0].strip()
                            o.StoreNum = row[1].strip()
                            o.firstname = row[2].strip()
                            o.lastname = row[3].strip()
                            o.company = row[4].strip()
                            o.address = row[5].strip()
                            o.city = row[6].strip()
                            o.state = row[7].strip()
                            o.zipcode = row[8].strip()
                            o.phone = row[9].strip()
                            o.email = row[10][:200].strip()
                            o.response = row[11].strip()
                            o.projectname = row[12].strip()
                            o.projectduedate = row[13].strip()
                            o.projectdetails = row[14].strip()
                            o.offer = row[15].strip()
                            o.submit = row[16].strip()
                            o.ServerTime = dt.date()
                            o.ServerDateTime = dt
                            o.misc1 = row[18].strip()
                            o.misc2 = row[19].strip()
                            o.misc3 = row[20].strip()
                            o.misc4 = row[21].strip()
                            o.misc5 = row[22].strip()


                            try:
                                o.save()
                                iNewRecords += 1
                            except:
                                logging.warning("unknown save error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                                print row
                                print sPseudoId
                                print sorted(dExisting[sDate])
                                print "likely dup"
                                raise

                            dExisting[ sDate][sPseudoId] = True



        #transaction.commit()
    return iNewRecords


#@transaction.commit_manually
def loadVoiceStarCSV(lsSDates=[], autofetch=True, forceupdate=False):
    """
    todo: transactions?

    autofetch = download if file doesn't exit
    """

    iNewRecords = 0

    for sDate in lsSDates:
        dtDate = dateutil.parser.parse(sDate)
        #!!!! can't get tz from VoiceStar currently, so assuming everything incoming is Eastern, when it isn't
        # and to complicate things, we want to store everything in the db as UTC... joy
        #dtDate = dtDate.replace(tzinfo=etz)

        ### note that the actual date values in a CSV are for some tz, couldn't tell you which one
        ###   but what happens is the 04/02 csv will have calls from 4/1 late evening around midnight
        ###   To workaround, just expand the range wider than a strict 24 hours

        dtAfter = toUTC(dtDate - datetime.timedelta(hours=12), etz)
        dtBefore = toUTC(dtDate + datetime.timedelta(days=1, hours=12), etz)

        existingCallIds = models.VoiceStarCallLog.objects.filter(call_s__gte=dtAfter, call_s__lte=dtBefore).values_list("call_id", flat=True)
        dExisting = collections.defaultdict(set)

        ### another pain from not knowing specific tz is that it's very hard to accurately prune
        ###   To workaround, keep track of the range of dates we see in a csv, then compare to what we have in THAT timerange
        ###   NOTE: this *will miss* those that were on the fringe (before or after the new range)
        sDTRange = set()

        for vals in existingCallIds:
            dExisting[sDate].add(vals)

        #print dExisting

        file_path = REPORT_DL_PATH + "VoiceStar/" + sDate + "_voicestar.csv"
        print file_path
        if forceupdate:
            dlVoiceStarReports([sDate], force=True)   
            try:
                p = os.stat(file_path)
            except:
                transaction.rollback()
                raise

        else:

            try:
                p = os.stat(file_path)
            except:

                if autofetch:
                    logging.warning(["!! Trying to fetch, doesn't exist on fs", sDate])
                    dlVoiceStarReports([sDate])   
                    try:
                        p = os.stat(file_path)
                    except:
                        transaction.rollback()
                        raise
                else:
                    transaction.rollback()
                    return

        #print '1'

        with open(file_path, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)
            dHeaderLookup = {}
            #print '1'
            latestIds = set()
            for i, row in enumerate(csvreader):
                
                if i % 1000 == 0: print i, "voicestar"

                #print ', '.join(row)
                #print row
                #print

                #TODO: move row column numbers to lookups to better handle csv changes in the future
                if len(row) != 0 and i == 0:
                    for iCol, sColName in enumerate(row):
                        dHeaderLookup[sColName] = iCol

                
                if len(row) != 0 and i != 0:
                    sPseudoId = row[2]
                    latestIds.add(sPseudoId)
                    #print sPseudoId
                    #print row
                    o = None
                    isNew = False
                    if sPseudoId not in dExisting[sDate]:
                        #print parser.parse(row[1]).date(), existingDates, sCustId
                        #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                        o = models.VoiceStarCallLog()
                    elif forceupdate:
                        o, bCreated = models.VoiceStarCallLog.objects.get_or_create(call_id__exact=row[2])

                    #print parser.parse(row[1]).date(), existingDates, sCustId
                    if o:
                        #print parser.parse(row[1]).date(), existingDates, sCustId
                        #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                        
                        if not o.id:
                            isNew = True

                        o.caller_number = row[0]
                        o.caller_name = row[1]
                        o.call_id = row[2]
                        o.inbound_no = row[3]
                        o.inbound_ext = row[4][:25]  # quick fix for asshats who post not legit ext
                        o.keyword = row[5]
                        o.forward_no = row[6]
                        o.custom_id = row[7]
                        o.account_id = row[8]
                        o.group_id = row[9]
                        o.campaign_id = row[10]
                        o.a_name = row[11]
                        o.g_name = row[12]
                        o.c_name = row[13]
                        #!!!
                        dtLocalTime = dateutil.parser.parse(row[14])
                        dtCall = toUTC(dateutil.parser.parse(row[14]), etz)
                        o.call_s = dtCall
                        sDTRange.add(dtCall)

                        lsDurationParts = [int(x) for x in row[15].split(":")]
                        iDuration = 60*60*lsDurationParts[0] + 60*lsDurationParts[1] + lsDurationParts[2] 
                        o.duration = iDuration

                        lsOffsetParts = [int(x) for x in row[16].split(":")]
                        iOffset = 60*60*lsOffsetParts[0] + 60*lsOffsetParts[1] + lsOffsetParts[2]
                        o.answer_offset = iOffset

                        o.call_status = row[17]
                        o.disposition = row[18]
                        o.rating = row[19]
                        o.listenedto = bool(int(row[dHeaderLookup['listenedto']])) 
                        o.dna_class = row[dHeaderLookup['dna_class']]

                        o.is_spam = o.duration < CALL_SPAM_SEC_DURATION \
                            or CALL_SPAM_OK_START_TIME > dtLocalTime.time() \
                            or CALL_SPAM_OK_END_TIME < dtLocalTime.time() \
                            or CALL_SPAM_CALL_STATUS_NOFORWARDS == o.call_status

                        try:
                            o.save()
                            if isNew:
                                iNewRecords += 1
                        except:
                            logging.warning("unknown save error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                            print row
                            print sPseudoId
                            print sorted(dExisting[sDate])
                            print "likely dup"
                            raise

                        dExisting[ sDate].add(sPseudoId)


        # if forceupdate:
        #     ##remove those that the system has pruned
        #     lsSortedRange = sorted(sDTRange)
        #     if lsSortedRange:
        #         dtCSVAfter = lsSortedRange[0]
        #         dtCSVBefore = lsSortedRange[-1]
        #         print dtCSVAfter, dtCSVBefore
        #         existingCallIdsCSVRange = models.VoiceStarCallLog.objects.filter(call_s__gte=dtCSVAfter, call_s__lte=dtCSVBefore).values_list("call_id", flat=True)
            

        #         sPruneThese = set(existingCallIdsCSVRange).difference(latestIds)
        #         print sPruneThese
                ### THIS DOESN"T WORK.  The reports overlap.  So the range we get from a CSV may actually cross over into the previous or post day's CSV.  Ignoreing for now

        #transaction.commit()
        #transaction.rollback()
    return iNewRecords


##@transaction.commit_on_success
@transaction.commit_manually
def loadCSV(sCustId, sType, lsSDates=[], autofetch=True, forceupdate=False):
    """
    todo: transactions?

    autofetch = download if file doesn't exit
    """

    

    for sDate in lsSDates:
        if sType== "account":
            existingDates = models.GoogleAccountPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId),Date__exact=dateutil.parser.parse(sDate).date()).values_list("Date","AdNetworkType1", "AdNetworkType2", "Device","ClickType")
            dExisting = collections.defaultdict(set)

            for vals in existingDates:
                dExisting[vals[0]].add(u'_'.join(vals[1:]))

            #print dExisting

            file_path = REPORT_DL_PATH + sCustId + "/" + dReportSpecs[sType]['file_prefix'] + sCustId + '_' + sDate + '.csv'

            #if forcefetch:

            if forceupdate:
                try:
                    dlReports(sType, [sCustId], [sDate], force=True) 
                except (AdWordsReportError,), e:
                    #ALSO HAS e.trigger and e.field_path
                    logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                    if hasattr(e, 'http_code') and e.http_code == 400 and e.type == 'ReportDefinitionError.CUSTOMER_SERVING_TYPE_REPORT_MISMATCH':

                        ## bad account id from what I can tell - try 5882371767
                        transaction.rollback()
                        return

                        
                    else:
                        transaction.rollback()
                        raise
                except:
                    transaction.rollback()
                    raise

                try:
                    p = os.stat(file_path)
                except:
                    transaction.rollback()
                    raise

            else:
                try:
                    p = os.stat(file_path)
                except:

                    if autofetch:
                        logging.warning(["!! Trying to fetch, doesn't exist on fs", sCustId, sType, sDate])
                        try:
                            dlReports(sType, [sCustId], [sDate]) 
                        except (AdWordsReportError), e:
                            #ALSO HAS e.trigger and e.field_path
                            logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                            
                            if hasattr(e, 'http_code') and e.http_code == 400 and e.type == 'ReportDefinitionError.CUSTOMER_SERVING_TYPE_REPORT_MISMATCH':
                                ## bad account id from what I can tell - try 5882371767
                                transaction.rollback()
                                return

                        
                            else:
                                transaction.rollback()
                                raise
                        except:
                            transaction.rollback()
                            raise 

                        try:
                            p = os.stat(file_path)
                        except:
                            transaction.rollback()
                            raise
                    else:
                        transaction.rollback()
                        return


            with open(file_path, 'rb') as csvfile:
                csvreader = csv.reader(csvfile)
                for i, row in enumerate(csvreader):
                    if i % 10000 == 0: print i, sCustId, "acct"

                    #print ', '.join(row)
                    
                    if row[0].strip() != "Total" and i not in [0,1]:
                        sPseudoId = u"_".join([unicode(x, 'utf-8') for x in row[11:15]])

                        o = None
                        if parser.parse(row[1]).date() not in dExisting.keys() or sPseudoId not in dExisting[parser.parse(row[1]).date()]:
                            #print parser.parse(row[1]).date(), existingDates, sCustId
                            #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                            o = models.GoogleAccountPerformanceReport()
                            logging.warning("newing it")
                        elif forceupdate:

                            o, bCreated = models.GoogleAccountPerformanceReport.objects.get_or_create(ExternalCustomerId__exact=int(sCustId),Date__exact=dateutil.parser.parse(sDate).date(), 
                              #CampaignId__exact=int(row[6]),
                              AdNetworkType1__exact=row[11], AdNetworkType2__exact=row[12], Device__exact=row[13], ClickType__exact=row[14])
                            
                            logging.warning("got it here")

                        if o:
                            #print parser.parse(row[1]).date(), existingDates, sCustId
                            #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                            #o = models.GoogleAccountPerformanceReport()
                            
                            try:
                                o.AccountDescriptiveName = row[0]
                                o.Date = parser.parse(row[1]).date()  #models.DateField('Date')
                                o.AccountCurrencyCode = row[2]
                                o.AccountId = int(row[3])
                                o.AccountTimeZoneId = row[4]
                                o.Impressions = int(row[5])
                                o.Clicks = int(row[6])
                                o.Ctr = float(row[7].replace("%", ""))
                                o.AverageCpc = Decimal(row[8])/1000000
                                o.Cost = Decimal(row[9].replace(",",""))/1000000
                                o.AveragePosition = float(row[10])
                                o.ExternalCustomerId = int(row[3])
                                o.AdNetworkType1 = row[11]
                                o.AdNetworkType2 = row[12]
                                o.Device = row[13]
                                o.ClickType = row[14]
                                o.Conversions = int(float(row[15]))  # was known as ConvertedClicks
                                o.CostPerConversion = Decimal(row[16])/1000000  # was known as CostPerConvertedClick
                                o.ConversionRate = float(row[17].replace("%", ""))  # was known as ClickConversionRate
                                o.TotalConvValue = float(row[18].replace(",",""))
                                o.ViewThroughConversions = int(row[19])
                                o.ValuePerConversion = float(row[20].replace(",",""))  # was known as ValuePerConvertedClick
                               
                            
                                o.save()
                            except:
                                logging.warning("unknown save error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                                print row
                                print sPseudoId
                                print sorted(dExisting[parser.parse(row[1]).date()])
                                print "likely dup"
                                raise

                            dExisting[o.Date].add(sPseudoId)

            transaction.commit()

        elif sType== "campaign":
            existingDates = set(models.GoogleCampaignPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId),Date__exact=dateutil.parser.parse(sDate).date()).values_list('Date','CampaignId',"AdNetworkType1", "AdNetworkType2","ClickType"))
            dExisting = collections.defaultdict(set)

            for vals in existingDates:
                dExisting[vals[0]].add(unicode(vals[1])  + u"_" + u'_'.join(vals[2:] ))


            file_path = REPORT_DL_PATH + sCustId + "/" + dReportSpecs[sType]['file_prefix'] + sCustId + '_' + sDate + '.csv'

            if forceupdate:
                try:
                    dlReports(sType, [sCustId], [sDate], force=True) 
                except (AdWordsReportError), e:
                    #ALSO HAS e.trigger and e.field_path
                    logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                    
                    if hasattr(e, 'http_code') and e.http_code == 400 and e.type == 'ReportDefinitionError.CUSTOMER_SERVING_TYPE_REPORT_MISMATCH':
                        ## bad account id from what I can tell - try 5882371767
                        transaction.rollback()
                        return

                        
                    else:
                        transaction.rollback()
                        raise
                except:
                    transaction.rollback()
                    raise
                try:
                    p = os.stat(file_path)
                except:
                    transaction.rollback()
                    raise

            else:
                try:
                    p = os.stat(file_path)
                except:

                    if autofetch:
                        logging.warning(["!! Trying to fetch, doesn't exist on fs", sCustId, sType, sDate])
                        try:
                            dlReports(sType, [sCustId], [sDate]) 
                        except (AdWordsReportError), e:
                            #ALSO HAS e.trigger and e.field_path
                            logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                            
                            if hasattr(e, 'http_code') and e.http_code == 400 and e.type == 'ReportDefinitionError.CUSTOMER_SERVING_TYPE_REPORT_MISMATCH':
                                ## bad account id from what I can tell - try 5882371767
                                transaction.rollback()
                                return

                                
                            else:
                                transaction.rollback()
                                raise
                        except:
                            transaction.rollback()
                            raise  
                        try:
                            p = os.stat(file_path)
                        except:
                            transaction.rollback()
                            raise
                    else:
                        transaction.rollback()
                        return


            iPending = 0
            with open(file_path, 'rb') as csvfile:
                csvreader = csv.reader(csvfile)
                for i, row in enumerate(csvreader):
                    if i % 10000 == 0: print i, sCustId, "campaign"
                    print row

                    if iPending % 2000 == 0 and iPending != 0:
                        logging.info("-- committing --")
                        transaction.commit()
                        
                        ## might want this if memory keeps leaking
                        #db.reset_queries()

                        iPending = 0

                    #print ', '.join(row)
                    
                    if row[0].strip() != "Total" and i not in [0,1]:
                        #print parser.parse(row[1]).date(), existingDates, sCustId
                        sPseudoId = unicode(row[5], 'utf-8') + u"_" + u"_".join([unicode(x, 'utf-8') for x in row[20:23]])
                        o = None
                        if parser.parse(row[1]).date() not in dExisting.keys() or sPseudoId not in dExisting[parser.parse(row[1]).date()]:
                            #print parser.parse(row[1]).date(), existingDates, sCustId
                            #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                            o = models.GoogleCampaignPerformanceReport()
                            logging.warning("newing it")
                        elif forceupdate:

                            o, bCreated = models.GoogleCampaignPerformanceReport.objects.get_or_create(ExternalCustomerId__exact=int(sCustId),Date__exact=dateutil.parser.parse(sDate).date(), 
                                CampaignId__exact=int(row[5]),AdNetworkType1__exact=row[20], AdNetworkType2__exact=row[21],ClickType__exact=row[22])
                            print "ere", bCreated, int(row[5]), row[20], row[21], row[22]
                            logging.warning("got it here")

                        if o:
                            iPending += 1
                            o.ExternalCustomerId = int(row[0])
                            o.Date = parser.parse(row[1]).date()  #models.DateField('Date')
                            o.AccountDescriptiveName = row[2]
                            o.AccountCurrencyCode = row[3]
                            o.AccountId = int(row[0])
                            o.AccountTimeZoneId = row[4]
                            o.CampaignId = int(row[5])
                            o.CampaignName = row[6]
                            o.CampaignStatus = row[7]
                            o.Impressions = int(row[8])
                            o.Clicks = int(row[9])
                            o.Ctr = float(row[10].replace("%", ""))
                            o.AverageCpc = Decimal(row[11])/1000000
                            o.Cost = Decimal(row[12].replace(",",""))/1000000
                            o.AveragePosition = float(row[13])
                            o.Conversions = int(float(row[14]))  # now known as ConvertedClicks
                            o.CostPerConversion = Decimal(row[15])/1000000  # now known as CostPerConvertedClick
                            o.ConversionRate = float(row[16].replace("%", ""))  # now known as ClickConversionRate
                            o.TotalConvValue = float(row[17].replace(",",""))
                            o.ViewThroughConversions = int(row[18])
                            o.ValuePerConversion = float(row[19].replace(",",""))  # now known as ValuePerConvertedClick
                            o.AdNetworkType1 = row[20]
                            o.AdNetworkType2 = row[21]
                            #o.Device = row[14]
                            o.ClickType = row[22]
                            try:
                                o.save()
                            except:
                                logging.warning("unknown save error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                                print row
                                print "likely dup"
                                raise
              

                            dExisting[o.Date].add(sPseudoId)

            if iPending > 0:
                transaction.commit()
            else:
                transaction.rollback()
                

        elif sType== "keyword":
            existingDates = models.GoogleKeywordPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId),Date__exact=dateutil.parser.parse(sDate).date()).values_list('Date',"AdGroupId", "KeywordId","AdNetworkType1", "AdNetworkType2", "Device","ClickType")
            dExisting = collections.defaultdict(set)

            for vals in existingDates:
                dExisting[vals[0]].add(unicode(vals[1]) + u"_" + unicode(vals[2]) + "_" + '_'.join(vals[3:]))

            file_path = REPORT_DL_PATH + sCustId + "/" + dReportSpecs[sType]['file_prefix'] + sCustId + '_' + sDate + '.csv'

            if forceupdate:
                try:
                    dlReports(sType, [sCustId], [sDate], force=True) 
                except (AdWordsReportError), e:
                    #ALSO HAS e.trigger and e.field_path
                    logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                    
                    if hasattr(e, 'http_code') and e.http_code == 400 and e.type == 'ReportDefinitionError.CUSTOMER_SERVING_TYPE_REPORT_MISMATCH':
                        ## bad account id from what I can tell - try 5882371767
                        transaction.rollback()
                        return

                        
                    else:
                        transaction.rollback()
                        raise
                except:
                    transaction.rollback()
                    raise
                try:
                    p = os.stat(file_path)
                except:
                    transaction.rollback()
                    raise

            else:
                try:
                    p = os.stat(file_path)
                except:

                    if autofetch:
                        logging.warning(["!! Trying to fetch, doesn't exist on fs", sCustId, sType, sDate])
                        try:
                            dlReports(sType, [sCustId], [sDate]) 
                        except (AdWordsReportError), e:
                            #ALSO HAS e.trigger and e.field_path
                            logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                            
                            if hasattr(e, 'http_code') and e.http_code == 400 and e.type == 'ReportDefinitionError.CUSTOMER_SERVING_TYPE_REPORT_MISMATCH':
                                ## bad account id from what I can tell - try 5882371767
                                transaction.rollback()
                                return

                                
                            else:
                                transaction.rollback()
                                raise
                        except:
                            transaction.rollback()
                            raise
                        try:
                            p = os.stat(file_path)
                        except:
                            transaction.rollback()
                            raise
                    else:
                        transaction.rollback()
                        return

            iPending = 0
            with open(file_path, 'rb') as csvfile:
                csvreader = csv.reader(csvfile)


                for i, row in enumerate(csvreader):
                    

                    if i % 10000 == 0: print i, sCustId, "kw"


                    if iPending % 500 == 0 and iPending != 0:
                        logging.info("-- committing --")
                        transaction.commit()
                        
                        ## might want this if memory keeps leaking
                        db.reset_queries()

                        iPending = 0


                   

                    #print ', '.join(row)
                    
                    if row[0].strip() != "Total" and i not in [0,1]:
                        
                        #print parser.parse(row[1]).date(), existingDates, sCustId

                        sPseudoId = unicode(row[8], 'utf-8') + "_" + unicode(row[11], 'utf-8') +u"_" +  u"_".join([unicode(x, 'utf-8') for x in row[26:30]])
                        o = None
                        if parser.parse(row[1]).date() not in dExisting.keys() or sPseudoId not in dExisting[parser.parse(row[1]).date()]:
                            #print parser.parse(row[1]).date(), existingDates, sCustId
                            #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                            o = models.GoogleKeywordPerformanceReport()
                            logging.warning("newing it")
                        elif forceupdate:

                            o, bCreated = models.GoogleKeywordPerformanceReport.objects.get_or_create(ExternalCustomerId__exact=int(sCustId),
                                            Date__exact=dateutil.parser.parse(sDate).date(), 
                                            AdGroupId__exact=int(row[8]),
                                            KeywordId__exact=int(row[11]),
                                            AdNetworkType1__exact=row[26], 
                                            AdNetworkType2__exact=row[27],
                                            Device__exact=row[28],
                                            ClickType__exact=row[29])
                            print "ere", bCreated, int(row[8]), row[11], row[26], row[27],row[28],row[29]
                            logging.warning("got it here")

                        if o:



                        #if parser.parse(row[1]).date() not in dExisting.keys() or sPseudoId not in dExisting[parser.parse(row[1]).date()]:
                            #print parser.parse(row[1]).date(), existingDates, sCustId
                            #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position


                            iPending += 1
                            #o = models.GoogleKeywordPerformanceReport()
                            o.ExternalCustomerId = int(row[0])
                            o.Date = parser.parse(row[1]).date()  #models.DateField('Date')
                            o.AccountDescriptiveName = row[2]
                            o.AccountCurrencyCode = row[3]
                            o.AccountTimeZoneId = row[4]
                            o.CampaignId = int(row[5])
                            o.CampaignName = row[6]
                            o.CampaignStatus = row[7]
                            o.AdGroupId = int(row[8])
                            o.AdGroupName = row[9]
                            o.AdGroupStatus = row[10]
                            o.KeywordId = int(row[11])
                            o.KeywordText = row[12]  # now known as Criteria
                            o.KeywordMatchType = row[13]

                            o.Impressions = int(row[14])
                            o.Clicks = int(row[15])
                            o.Ctr = float(row[16].replace("%", ""))
                            o.AverageCpc = Decimal(row[17])/1000000
                            o.Cost = Decimal(row[18].replace(",",""))/1000000
                            o.AveragePosition = float(row[19])
                            o.Conversions = int(float(row[20]))  # now known as ConvertedClicks
                            o.CostPerConversion = Decimal(row[21])/1000000  # now known as CostPerConvertedClick
                            o.ConversionRate = float(row[22].replace("%",""))  # now known as ClickConversionRate
                            o.TotalConvValue = float(row[23].replace(",",""))
                            o.ViewThroughConversions = int(row[24])
                            o.ValuePerConversion = float(row[25].replace(",",""))  # now known as ValuePerConvertedClick
                            o.AdNetworkType1 = row[26]
                            o.AdNetworkType2 = row[27]
                            o.Device = row[28]
                            o.ClickType = row[29]
                            try:
                                o.save()
                            except:
                                logging.warning("unknown save error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                                print row
                                print "likely dup"
                                raise
              

                            dExisting[o.Date].add(sPseudoId)

            if iPending > 0:
                transaction.commit()
            else:
                transaction.rollback()

        elif sType== "geo":
            #existingDates = set([o.Date for o in models.GoogleGeoPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId))])
            existingDates = models.GoogleGeoPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId),Date__exact=dateutil.parser.parse(sDate).date()).values_list('Date',"AdGroupId", "LocationType", "CountryCriteriaId", "RegionCriteriaId", "MetroCriteriaId", "CityCriteriaId","AdNetworkType1", "AdNetworkType2", "Device") ##, flat=True))
            dExisting = collections.defaultdict(set)

            for vals in existingDates:
                dExisting[vals[0]].add(unicode(vals[1]) + u"_" + u"_".join(vals[2:]))

            #print dExisting.items()[0]

            file_path = REPORT_DL_PATH + sCustId + "/" + dReportSpecs[sType]['file_prefix'] + sCustId + '_' + sDate + '.csv'
            if forceupdate:
                try:
                    dlReports(sType, [sCustId], [sDate], force=True) 
                except (AdWordsReportError), e:
                    #ALSO HAS e.trigger and e.field_path
                    logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                    
                    if hasattr(e, 'http_code') and e.http_code == 400 and e.type == 'ReportDefinitionError.CUSTOMER_SERVING_TYPE_REPORT_MISMATCH':
                        ## bad account id from what I can tell - try 5882371767
                        transaction.rollback()
                        return

                        
                    else:
                        transaction.rollback()
                        raise
                except:
                    transaction.rollback()
                    raise
                try:
                    p = os.stat(file_path)
                except:
                    transaction.rollback()
                    raise

            else:

                try:
                    p = os.stat(file_path)
                except:

                    if autofetch:
                        logging.warning(["!! Trying to fetch, doesn't exist on fs", sCustId, sType, sDate])
                        try:
                            dlReports(sType, [sCustId], [sDate]) 
                        except (AdWordsReportError), e:
                            #ALSO HAS e.trigger and e.field_path
                            logging.warning(u"API Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                            
                            if hasattr(e, 'http_code') and e.http_code == 400 and e.type == 'ReportDefinitionError.CUSTOMER_SERVING_TYPE_REPORT_MISMATCH':
                                ## bad account id from what I can tell - try 5882371767
                                transaction.rollback()
                                return

                                
                            else:
                                transaction.rollback()
                                raise
                        except:
                            transaction.rollback()
                            raise  
                        try:
                            p = os.stat(file_path)
                        except:
                            transaction.rollback()
                            raise
                    else:
                        transaction.rollback()
                        return

            iPending = 0
            with open(file_path, 'rb') as csvfile:
                csvreader = csv.reader(csvfile)
                for i, row in enumerate(csvreader):
                    if i % 10000 == 0: print i, sCustId, "geo"


                    if iPending % 500 == 0 and iPending != 0:
                        logging.info("-- committing --")
                        transaction.commit()

                        
                        ## might want this if memory keeps leaking
                        #db.reset_queries()



                        iPending = 0


                

                    #print ', '.join(row)
                    
                    if row[0].strip() != "Total" and i not in [0,1]:
                        
                        sPseudoId = unicode(row[8], 'utf-8') +u"_" + u"_".join([unicode(x, 'utf-8') for x in row[11:16]]) + u"_" + u"_".join([unicode(x, 'utf-8') for x in row[28:31]])
                        if parser.parse(row[1]).date() not in dExisting.keys() or sPseudoId not in dExisting[parser.parse(row[1]).date()]:

                            #print sPseudoId
                            iPending += 1
                            #print parser.parse(row[1]).date(), sCustId

                            o = models.GoogleGeoPerformanceReport()
                            o.ExternalCustomerId = int(row[0])
                            o.Date = parser.parse(row[1]).date()  #models.DateField('Date')
                            o.AccountDescriptiveName = row[2]
                            o.AccountCurrencyCode = row[3]
                            o.AccountTimeZoneId = row[4]
                            o.CampaignId = int(row[5])
                            o.CampaignName = row[6]
                            o.CampaignStatus = row[7]
                            o.AdGroupId = int(row[8])
                            o.AdGroupName = row[9]
                            o.AdGroupStatus = row[10]

                            o.LocationType = row[11]
                            o.CountryCriteriaId = row[12]
                            o.RegionCriteriaId = row[13]
                            o.MetroCriteriaId = row[14]
                            o.CityCriteriaId = row[15]

                            o.Impressions = int(row[16])
                            o.Clicks = int(row[17])
                            o.Ctr = float(row[18].replace("%", ""))
                            o.AverageCpc = Decimal(row[19])/1000000
                            o.Cost = Decimal(row[20].replace(",",""))/1000000
                            o.AveragePosition = float(row[21])
                            o.Conversions = int(float(row[22]))  # now known as ConvertedClicks
                            o.CostPerConversion = Decimal(row[23])/1000000  # now known as CostPerConvertedClick
                            o.ConversionRate = float(row[24].replace("%",""))  # now known as ClickConversionRate
                            o.TotalConvValue = float(row[25].replace(",",""))
                            o.ViewThroughConversions = int(row[26])
                            o.ValuePerConversion = float(row[27].replace(",",""))  # now known as ValuePerConvertedClick
                            o.AdNetworkType1 = row[28]
                            o.AdNetworkType2 = row[29]
                            o.Device = row[30]
                            #o.ClickType = row[15]
                            try:
                                o.save()
                            except:
                                logging.warning("unknown save error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                                print row
                                print "likely dup"
                                raise
              

                            dExisting[o.Date].add(sPseudoId)


            if iPending > 0:
                transaction.commit()
            else:
                transaction.rollback()


def printt(*args):
   logging.warning(args)


def loadCSVByDates(lsCustIds, lsSDates, force=False, lsTypes=None):
    logging.warning(lsCustIds)
    logging.warning(lsSDates)
    sIgnoreThisCust = set()

    dbrpool = eventlet.GreenPool(4)
    if not lsTypes:
        lsTypes = sorted(dReportSpecs.keys())

    for sReportType in lsTypes:
        logging.warning("loadCSVByDates report type: %s" % sReportType)
        for sCustId in sorted(lsCustIds):
            if sCustId not in sIgnoreThisCust:
                logging.warning("loadCSVByDates custid: %s" % sCustId)
                #dbrpool.spawn_n(loadCSV, sCustId, sReportType, lsSDates, True, force)
                #dbrpool.spawn_n(printt, sCustId, sReportType, lsSDates, True, force)
                #loadCSV(sCustId, sReportType, lsSDates, True, forceupdate=True)
                        
                iTries = 0
                while iTries < 6:
                    try:
                        loadCSV(sCustId, sReportType, lsSDates, True, forceupdate=True)
                        break
                    # except ValidationError:
                    #     logging.warning(["Auth Error - believe this is due to client turnover", sCustId, sReportType])
                    #     sIgnoreThisCust.add(sCustId)
                    #     break
                    #     #TODO - maybe mark as inactive??
                    except:
                        logging.warning("yo")
                        logging.warning(u"Unknown retryable error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                        iTries += 1
                        time.sleep(iTries * 2)
                if iTries >= 6:
                    raise Exception("OOOPS")

            
        logging.warning("loadCSVByDates report done: %s" % sReportType)
        

from xlwt import Workbook, XFStyle, Borders, Pattern, Font, easyxf   


lsAGHistoricalLabels = [
        u"",
        u"Impressions",
        u"Clicks", 
        u"CTR", 
        u"Avg. CPC", 
        u"Media",
        u"Total", 
        u"Calls",
        u"Emails",
        u"Contacts",
        u"Contact %",
        u"Cost/Contact"
    ]

lsAGSummaryLabels = [
  u"Center",
  u"Sum of Call",
  u"Sum of Email",
  u"Sum of Contacts"

]    

lsAGKeywordLabels = [
  u"Campaign",
  u"Ad Group",
  u"Keyword",
  u"Match Type",
  u"Impressions",
  u"Clicks",
  u"CTR",
  u"Avg CPC",
  u"Cost",
  u"Avg Position"
]

dCellStyles = {}
for i, fontExtra in enumerate([", bold true", ""]):
    if i == 0:
        k = "bold_"
    else:
        k = ""
    dCellStyles[k+"dollar"] = easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = '$#,##0.00')
    dCellStyles[k+"dollarwhole"] = easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = '"$"#,##0_);("$"#,##')
    dCellStyles[k+"number"] = easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = '#,##0')
    
    dCellStyles[k+"percent"] = easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = '0.00%')
    dCellStyles[k+"default"] = easyxf('font: name Calibri, height 220%s;' % fontExtra)


def Sheet_AG_Group_KW(sheet, groupId, iMonth, iYear):

    




    def _outputRowArgs(d, bold=False):

        if d['Impressions']:
            CTR = float(d['Clicks'])/float(d['Impressions'])
        else:
            CTR = 0.0

        if d['Clicks']:
            avgCPC = float(d["Cost"])/float(d['Clicks'])
        else:
            avgCPC = 0.0

        if sum([x[1] for x in d["AvgPosAndClicks"]]) > 0:
            avgPos = "%.2f" % (sum([x[1] * x[0] for x in d["AvgPosAndClicks"]])/float(sum([x[1] for x in d["AvgPosAndClicks"]])))
        else:
            avgPos = "%.2f" % 0.0

        if d.has_key('Conversions') and d['Conversions']:
            costPerConv = float(d['Cost'])/float(d['Conversions'])
        else:
            costPerConv = 0.0

        if d.has_key('Conversions') and d['Conversions'] and d['Clicks']:
            convRate = float(d['Conversions'])/float(d['Clicks'])
        else:
            convRate = 0.0


        if d.has_key('ConversionValue') and d["ConversionValue"] and d['Cost']:
            convValueCost = float(d["ConversionValue"])/float(d["Cost"])
        else:
            convValueCost = 0.0



        rowFormatted = [
            d['CampaignName'], 
            d["AdGroupName"],
            d["KeywordText"],
            d["KeywordMatchType"],
            d['Impressions'], 
            d['Clicks'],
            #"%.5f" % (float(d['Clicks'])/float(d['Impressions']),),
            CTR,
            #"%.2f" % avgCPC,
            avgCPC,
            d['Cost'],
            avgPos,
            # #avgPos,
            # d['Conversions'],
            # #"%.2f" % costPerConv,
            # costPerConv,
            # #"%.2f" % convRate,
            # convRate,
            # d["ViewThroughConversions"],
            # d["ConversionValue"],
            # "%.2f" % convValueCost,
            #"NA",
            #"NA",
            #"NA",
            #d["ConversionValue"]       
        ]
        #print rowFormatted

        if bold:
            kExtra = "bold_"
        else:
            kExtra = ""

        rowcols = []
        print rowFormatted
        for j, val in enumerate(rowFormatted):

            #logging.warning([i+2, j, val])
            if j in [7,8]:
                #print d 
                #rowcols.append([j, val, easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = CURRENCYCODE_TO_SYMBOL[d["AccountCurrencyCode"]]+'#,##0.00')])
                rowcols.append([j, val, dCellStyles[kExtra + "dollar"]])
            elif j in [6]:
                rowcols.append([j, val, dCellStyles[kExtra + "percent"]])
            else:
                rowcols.append([j, val, dCellStyles[kExtra + "default"]])

        return rowcols


    dtStartMonth = datetime.datetime(month=iMonth, year=iYear, day=1, tzinfo=pytz.utc)
    dtEnd = dtStartMonth+dateutil.relativedelta.relativedelta(months=+1)

    print dtStartMonth
    print dtEnd
    
    dKWAggr = {}

    oGroup = models.Group.objects.get(id=groupId)
    
    oGoogs = oGroup.account_set.filter(ServiceType__exact='1')
    ##oVSs = oGroup.account_set.filter(ServiceType__exact='2')

    oRows = models.GoogleKeywordPerformanceReport.objects.filter(ExternalCustomerId__in=[x.ServiceAccountId for x in oGoogs], Date__gte=dtStartMonth, Date__lt=dtEnd) #, KeywordText__exact=u'printing chicago')

    iLongestName = len("Campaign")

    # dTotal = {}
    # for groupvar in ['Total', ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
    #     dTotal[groupvar] = {
    #                 "CampaignName":ADNETWORKTYPE1_LABELS.get(groupvar, "Total"),
    #                 "Clicks":0,
    #                 "Impressions":0,
    #                 "Cost": 0,
    #                 "AvgPosAndClicks":[],
    #                 "Conversions":0,
    #                 "ViewThroughConversions":0,
    #                 "ConversionValue":0,
    #                 "AccountCurrencyCode":"USD"
    #             }

    for row in oRows:
        #if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #logging.warning([row.Date, row.CampaignName ])
        if not dKWAggr.has_key(str(row.CampaignId) + "_" + str(row.KeywordId)):
            dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)] = {
                "CampaignName":row.CampaignName,
                "AdGroupName":row.AdGroupName,
                "KeywordText":row.KeywordText,
                "KeywordMatchType":row.KeywordMatchType,
                "AccountCurrencyCode":row.AccountCurrencyCode,  #DEFAULT
                "Clicks":0,
                "Impressions":0,
                "Cost": 0,
                "AvgPosAndClicks":[],
                #"Conversions":0,
                #"ViewThroughConversions":0,
                #"ConversionValue":0
            }
            #for subtotalkey in ["Total", ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
            #    dTotal[subtotalkey]["AccountCurrencyCode"] = row.AccountCurrencyCode


        dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["Clicks"] += row.Clicks
        if row.ClickType in CLICKTYPES_TO_INCLUDE:
            dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["Impressions"] += row.Impressions
        dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["Cost"] += row.Cost
        #dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["Conversions"] += row.Conversions
        #dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["ViewThroughConversions"] += row.ViewThroughConversions
        #dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["ConversionValue"] += row.TotalConvValue
        if row.ClickType in CLICKTYPES_TO_INCLUDE:
            dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))
        
        # if row.AdNetworkType1 in [ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
        #     dTotal[row.AdNetworkType1]["Clicks"] += row.Clicks
        #     if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #         dTotal[row.AdNetworkType1]["Impressions"] += row.Impressions
        #     dTotal[row.AdNetworkType1]["Cost"] += row.Cost
        #     #dTotal[row.AdNetworkType1]["Conversions"] += row.Conversions
        #     #dTotal[row.AdNetworkType1]["ViewThroughConversions"] += row.ViewThroughConversions
        #     #dTotal[row.AdNetworkType1]["ConversionValue"] += row.TotalConvValue
        #     dTotal[row.AdNetworkType1]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

        # dTotal['Total']["Clicks"] += row.Clicks
        # if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #     dTotal['Total']["Impressions"] += row.Impressions
        # dTotal['Total']["Cost"] += row.Cost
        # dTotal['Total']["Conversions"] += row.Conversions
        # dTotal['Total']["ViewThroughConversions"] += row.ViewThroughConversions
        # dTotal['Total']["ConversionValue"] += row.TotalConvValue
        # dTotal['Total']["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

        if len(row.CampaignName) > iLongestName:
            iLongestName = len(row.CampaignName)

    #return dKWAggr


    styleHeader = easyxf(
        'font: name Calibri, colour white, height 220;'
        #'borders: left thick, right thick, top thick, bottom thick;'
        'pattern: pattern solid, fore_colour light_blue;',
        #num_format_str='YYYY-MM-DD'
    )

    #book = Workbook()
    #campsheet = book.add_sheet(u'Keyword')
    ##kwsheet = book.add_sheet(u'Keyword Report')

    #campsheet.write(0,0,u'Campaign Report - %s (%s - %s)' % (sAcctName, lsDates[0].strftime(u"%b %d"), lsDates[-1].strftime(u"%b %d")), easyxf('font: name Calibri, bold true, height 220;'))

    iWeekdayOfFirst, iDaysInMonth = calendar.monthrange(iYear,iMonth)
    sMonthAbbr = calendar.month_abbr[iMonth]

    sheet.write_merge(0,0, 0, 1, u'Keyword Report %s 1 - %i' % (sMonthAbbr, iDaysInMonth), dCellStyles["bold_default"])
    for i, sName in enumerate(lsAGKeywordLabels):
        sheet.write(1, i, sName, styleHeader)

    xtraWideCols = [1,2]
    sheet.col(0).width = 220 * 20 ##256 * iLongestName
    for i, label in enumerate(lsAGKeywordLabels):

        if i in xtraWideCols:
            sheet.col(i).width = 220 * 44
        elif not i == 0:
            sheet.col(i).width = 220 * max(15, len(label))
    

    i = 0  #just in case there are not items
    for i, (id, d) in enumerate(list(sorted(sorted(dKWAggr.iteritems(),key=lambda x: x[1]['CampaignName']), key=lambda x: x[1]['Clicks'], reverse=True))):
        lsRowcols = _outputRowArgs(d)
        for col in lsRowcols:
            sheet.write(i+2, *col)
    
    return sheet


def Sheet_AG_Group_KWv2(sheet, groupId, iMonth, iYear):

    




    def _outputRowArgs(d, bold=False):

        if d['Impressions']:
            CTR = float(d['Clicks'])/float(d['Impressions'])
        else:
            CTR = 0.0

        if d['Clicks']:
            avgCPC = float(d["Cost"])/float(d['Clicks'])
        else:
            avgCPC = 0.0

        if sum([x[1] for x in d["AvgPosAndClicks"]]) > 0:
            avgPos = "%.2f" % (sum([x[1] * x[0] for x in d["AvgPosAndClicks"]])/float(sum([x[1] for x in d["AvgPosAndClicks"]])))
        else:
            avgPos = "%.2f" % 0.0

        if d.has_key('Conversions') and d['Conversions']:
            costPerConv = float(d['Cost'])/float(d['Conversions'])
        else:
            costPerConv = 0.0

        if d.has_key('Conversions') and d['Conversions'] and d['Clicks']:
            convRate = float(d['Conversions'])/float(d['Clicks'])
        else:
            convRate = 0.0


        if d.has_key('ConversionValue') and d["ConversionValue"] and d['Cost']:
            convValueCost = float(d["ConversionValue"])/float(d["Cost"])
        else:
            convValueCost = 0.0



        rowFormatted = [
            d['CampaignName'], 
            d["AdGroupName"],
            d["KeywordText"],
            d["KeywordMatchType"],
            d['Impressions'], 
            d['Clicks'],
            #"%.5f" % (float(d['Clicks'])/float(d['Impressions']),),
            CTR,
            #"%.2f" % avgCPC,
            avgCPC,
            d['Cost'],
            avgPos,
            # #avgPos,
            # d['Conversions'],
            # #"%.2f" % costPerConv,
            # costPerConv,
            # #"%.2f" % convRate,
            # convRate,
            # d["ViewThroughConversions"],
            # d["ConversionValue"],
            # "%.2f" % convValueCost,
            #"NA",
            #"NA",
            #"NA",
            #d["ConversionValue"]       
        ]
        #print rowFormatted

        if bold:
            kExtra = "bold_"
        else:
            kExtra = ""

        rowcols = []
        print rowFormatted
        for j, val in enumerate(rowFormatted):

            #logging.warning([i+2, j, val])
            if j in [7,8]:
                #print d 
                #rowcols.append([j, val, easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = CURRENCYCODE_TO_SYMBOL[d["AccountCurrencyCode"]]+'#,##0.00')])
                rowcols.append([j, val, dCellStyles[kExtra + "dollar"]])
            elif j in [6]:
                rowcols.append([j, val, dCellStyles[kExtra + "percent"]])
            else:
                rowcols.append([j, val, dCellStyles[kExtra + "default"]])

        return rowcols


    dtStartMonth = datetime.datetime(month=iMonth, year=iYear, day=1, tzinfo=pytz.utc)
    dtEnd = dtStartMonth+dateutil.relativedelta.relativedelta(months=+1)

    print dtStartMonth
    print dtEnd
    
    dKWAggr = {}

    oGroup = models.AdAccountOwner.objects.get(id=groupId)
    oSubaccounts = [sa.subaccount for sa in oGroup.subaccounts.filter(subaccount__Active__exact=True)]


    # dSubAccountsByInternalId = dict([(sa.InternalId, sa) for sa in oSubaccounts])
    # dAdAccountsByInternalId = collections.defaultdict(lambda: collections.defaultdict(list))
    # dReverseVSIds = {}
    # for sa in oSubaccounts:
    #     dAdAccountsByInternalId[sa.InternalId][1] += [ac.AdAccount for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='1')]
    #     dAdAccountsByInternalId[sa.InternalId][2] += [ac.AdAccount for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='2')]
    #     for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='2'):
    #         dReverseVSIds[ac.AdAccount.ServiceAccountId] = sa.InternalId

    
    oGoogs = [ac.AdAccount for ac in oGroup.adaccounts.filter(AdAccount__ServiceType__exact='1', AdAccount__Active__exact=True)]
    # oVSs = []
    # for grp in [oGroup] + oSubaccounts:
    #    for ac in grp.adaccounts.filter(AdAccount__ServiceType__exact='2', AdAccount__Active__exact=True):
    #       oVSs.append(ac.AdAccount)

    
    # iLenVSs = len(oVSs)

    
    


    ###old ########
    #oGoogs = oGroup.account_set.filter(ServiceType__exact='1')
    ##oVSs = oGroup.account_set.filter(ServiceType__exact='2')

    oRows = models.GoogleKeywordPerformanceReport.objects.filter(ExternalCustomerId__in=[x.ServiceAccountId for x in oGoogs], Date__gte=dtStartMonth, Date__lt=dtEnd) #, KeywordText__exact=u'printing chicago')

    iLongestName = len("Campaign")

    # dTotal = {}
    # for groupvar in ['Total', ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
    #     dTotal[groupvar] = {
    #                 "CampaignName":ADNETWORKTYPE1_LABELS.get(groupvar, "Total"),
    #                 "Clicks":0,
    #                 "Impressions":0,
    #                 "Cost": 0,
    #                 "AvgPosAndClicks":[],
    #                 "Conversions":0,
    #                 "ViewThroughConversions":0,
    #                 "ConversionValue":0,
    #                 "AccountCurrencyCode":"USD"
    #             }

    for row in oRows:
        #if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #logging.warning([row.Date, row.CampaignName ])
        if not dKWAggr.has_key(str(row.CampaignId) + "_" + str(row.KeywordId)):
            dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)] = {
                "CampaignName":row.CampaignName,
                "AdGroupName":row.AdGroupName,
                "KeywordText":row.KeywordText,
                "KeywordMatchType":row.KeywordMatchType,
                "AccountCurrencyCode":row.AccountCurrencyCode,  #DEFAULT
                "Clicks":0,
                "Impressions":0,
                "Cost": 0,
                "AvgPosAndClicks":[],
                #"Conversions":0,
                #"ViewThroughConversions":0,
                #"ConversionValue":0
            }
            #for subtotalkey in ["Total", ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
            #    dTotal[subtotalkey]["AccountCurrencyCode"] = row.AccountCurrencyCode


        dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["Clicks"] += row.Clicks
        if row.ClickType in CLICKTYPES_TO_INCLUDE:
            dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["Impressions"] += row.Impressions
        dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["Cost"] += row.Cost
        #dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["Conversions"] += row.Conversions
        #dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["ViewThroughConversions"] += row.ViewThroughConversions
        #dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["ConversionValue"] += row.TotalConvValue
        if row.ClickType in CLICKTYPES_TO_INCLUDE:
            dKWAggr[str(row.CampaignId) + "_" + str(row.KeywordId)]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))
        
        # if row.AdNetworkType1 in [ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
        #     dTotal[row.AdNetworkType1]["Clicks"] += row.Clicks
        #     if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #         dTotal[row.AdNetworkType1]["Impressions"] += row.Impressions
        #     dTotal[row.AdNetworkType1]["Cost"] += row.Cost
        #     #dTotal[row.AdNetworkType1]["Conversions"] += row.Conversions
        #     #dTotal[row.AdNetworkType1]["ViewThroughConversions"] += row.ViewThroughConversions
        #     #dTotal[row.AdNetworkType1]["ConversionValue"] += row.TotalConvValue
        #     dTotal[row.AdNetworkType1]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

        # dTotal['Total']["Clicks"] += row.Clicks
        # if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #     dTotal['Total']["Impressions"] += row.Impressions
        # dTotal['Total']["Cost"] += row.Cost
        # dTotal['Total']["Conversions"] += row.Conversions
        # dTotal['Total']["ViewThroughConversions"] += row.ViewThroughConversions
        # dTotal['Total']["ConversionValue"] += row.TotalConvValue
        # dTotal['Total']["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

        if len(row.CampaignName) > iLongestName:
            iLongestName = len(row.CampaignName)

    #return dKWAggr


    styleHeader = easyxf(
        'font: name Calibri, colour white, height 220;'
        #'borders: left thick, right thick, top thick, bottom thick;'
        'pattern: pattern solid, fore_colour light_blue;',
        #num_format_str='YYYY-MM-DD'
    )

    #book = Workbook()
    #campsheet = book.add_sheet(u'Keyword')
    ##kwsheet = book.add_sheet(u'Keyword Report')

    #campsheet.write(0,0,u'Campaign Report - %s (%s - %s)' % (sAcctName, lsDates[0].strftime(u"%b %d"), lsDates[-1].strftime(u"%b %d")), easyxf('font: name Calibri, bold true, height 220;'))

    iWeekdayOfFirst, iDaysInMonth = calendar.monthrange(iYear,iMonth)
    sMonthAbbr = calendar.month_abbr[iMonth]

    sheet.write_merge(0,0, 0, 1, u'Keyword Report %s 1 - %i' % (sMonthAbbr, iDaysInMonth), dCellStyles["bold_default"])
    for i, sName in enumerate(lsAGKeywordLabels):
        sheet.write(1, i, sName, styleHeader)

    xtraWideCols = [1,2]
    sheet.col(0).width = 220 * 20 ##256 * iLongestName
    for i, label in enumerate(lsAGKeywordLabels):

        if i in xtraWideCols:
            sheet.col(i).width = 220 * 44
        elif not i == 0:
            sheet.col(i).width = 220 * max(15, len(label))
    

    i = 0  #just in case there are not items
    for i, (id, d) in enumerate(list(sorted(sorted(dKWAggr.iteritems(),key=lambda x: x[1]['CampaignName']), key=lambda x: x[1]['Clicks'], reverse=True))):
        lsRowcols = _outputRowArgs(d)
        for col in lsRowcols:
            sheet.write(i+2, *col)
    
    return sheet




from dateutil import rrule

def Sheet_AG_Group_Acct(sheet, groupId, iMonth, iYear):  #, dAcctNameLookups={}
    def _outputRowArgs(k, d, bold=False):

        if d['Impressions']:
            CTR = float(d['Clicks'])/float(d['Impressions'])
        else:
            CTR = 0.0

        if d['Clicks']:
            avgCPC = float(d["Cost"])/float(d['Clicks'])
        else:
            avgCPC = 0.0

        if sum([x[1] for x in d["AvgPosAndClicks"]]) > 0:
            avgPos = "%.1f" % (sum([x[1] * x[0] for x in d["AvgPosAndClicks"]])/float(sum([x[1] for x in d["AvgPosAndClicks"]])))
        else:
            avgPos = "%.1f" % 0.0

        if d.has_key('Emails') and d['Emails']:
            costPerConv = float(d['Cost'])/float(d['Emails'])
        else:
            costPerConv = 0.0

        if d.has_key('Emails') and d['Emails'] and d['Clicks']:
            convRate = float(d['Emails'])/float(d['Clicks'])
        else:
            convRate = 0.0


        if d.has_key('ConversionValue') and d["ConversionValue"] and d['Cost']:
            convValueCost = float(d["ConversionValue"])/float(d["Cost"])
        else:
            convValueCost = 0.0


        if d['Clicks']:
            print float(d['Calls'] + d['Emails'])/float(d['Clicks'])
            contactPercent = float(d['Calls'] + d['Emails'])/float(d['Clicks'])
        else:
            contactPercent = 0.0

        if d.has_key('Emails') and d['Calls'] + d['Emails']:
            costPerContact = float(d['Cost'])*F_MARKUP/float(d['Calls'] + d['Emails'])
        else:
            costPerContact = 0.0



        if d['Cost']:
          fMarkedUpTotalCost = max(F_MIN_AMOUNT,float(d['Cost']) * F_MARKUP)
        else:
          fMarkedUpTotalCost = 0.0

        rowFormatted = [
            k.strftime("%b"),
            d['Impressions'], 
            d['Clicks'], 
           
            #"%.5f" % (float(d['Clicks'])/float(d['Impressions']),),
            CTR,
            #"%.2f" % avgCPC,
            avgCPC,
            d['Cost'],
            fMarkedUpTotalCost,
            d['Calls'],
            #avgPos,
            d['Emails'],
            d['Calls'] + d['Emails'],
            #"%.2f" % costPerConv,
            contactPercent,
            costPerContact
                   
        ]
        #print rowFormatted

        if bold:
            kExtra = "bold_"
        else:
            kExtra = ""

        rowcols = []
        print rowFormatted
        for j, val in enumerate(rowFormatted):
            #logging.warning([i+2, j, val])
            if j in [4]:
                #print d 
                #rowcols.append([j, val, easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = CURRENCYCODE_TO_SYMBOL[d["AccountCurrencyCode"]]+'#,##0.00')])
                rowcols.append([j, val, dCellStyles[kExtra + "dollar"]])
            elif j in [5,6,11]:
                rowcols.append([j, val, dCellStyles[kExtra + "dollarwhole"]])
            elif j in [3,10]:
                rowcols.append([j, val, dCellStyles[kExtra + "percent"]])
            elif j in [1,2]:
                rowcols.append([j, val, dCellStyles[kExtra + "number"]])
            else:
                rowcols.append([j, val, dCellStyles[kExtra + "default"]])

        return rowcols

    
    styleHeader = easyxf(
        'font: name Calibri, colour white, height 220;'
        #'borders: left thick, right thick, top thick, bottom thick;'
        'pattern: pattern solid, fore_colour light_blue;',
        #num_format_str='YYYY-MM-DD'
    )

    styleSubheader = easyxf(
        'font: name Calibri, colour black, height 220;'
        #'borders: left thick, right thick, top thick, bottom thick;'
        'pattern: pattern solid, fore_colour pale_blue;',
        #num_format_str='YYYY-MM-DD'
    )



    dtStartMonth = datetime.datetime(month=iMonth, year=iYear, day=1, tzinfo=pytz.utc)
    dtEnd = dtStartMonth+dateutil.relativedelta.relativedelta(months=+1)
    dtHistoricalStartMonth = datetime.datetime(month=1, year=2011, day=1, tzinfo=pytz.utc)

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=dtHistoricalStartMonth, until=dtStartMonth):
        print dt.date()

    dAcctAggr = {}.fromkeys([dt.date() for dt in rrule.rrule(rrule.MONTHLY, dtstart=dtHistoricalStartMonth, until=dtStartMonth)])
    
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=dtHistoricalStartMonth, until=dtStartMonth):
        dAcctAggr[dt.date()] = {
                "AccountCurrencyCode":None,  #DEFAULT
                "Clicks":0,
                "Impressions":0,
                "Cost": 0,
                "AvgPosAndClicks":[],
                "Conversions":0,
                "ViewThroughConversions":0,
                "ConversionValue":0,
                "Calls":0,
                "Emails":0,

            }

    

    oGroup = models.Group.objects.get(id=groupId)
    
    oGoogs = oGroup.account_set.filter(ServiceType__exact='1')
    oVSs = list(oGroup.account_set.filter(ServiceType__exact='2'))
    iLenVSs = len(oVSs)

    
    oRows = models.GoogleAccountPerformanceReport.objects.filter(ExternalCustomerId__in=[x.ServiceAccountId for x in oGoogs], Date__gte=dtHistoricalStartMonth, Date__lt=dtEnd) 

    iLongestName = len("Campaign")

    # dTotal = {}
    # for groupvar in ['Total', ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
    #     dTotal[groupvar] = {
    #                 "CampaignName":ADNETWORKTYPE1_LABELS.get(groupvar, "Total"),
    #                 "Clicks":0,
    #                 "Impressions":0,
    #                 "Cost": 0,
    #                 "AvgPosAndClicks":[],
    #                 "Conversions":0,
    #                 "ViewThroughConversions":0,
    #                 "ConversionValue":0,
    #                 "AccountCurrencyCode":"USD"
    #            }

    for row in oRows:
        #if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #logging.warning([row.Date, row.CampaignName ])
        # if not dAcctAggr.has_key(row.CampaignId):
        #     dAcctAggr[row.CampaignId] = {
        #         "CampaignName":row.CampaignName,
        #         "AccountCurrencyCode":row.AccountCurrencyCode,  #DEFAULT
        #         "Clicks":0,
        #         "Impressions":0,
        #         "Cost": 0,
        #         "AvgPosAndClicks":[],
        #         "Conversions":0,
        #         "ViewThroughConversions":0,
        #         "ConversionValue":0
        #     }
        #     for subtotalkey in ["Total", ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
        #         dTotal[subtotalkey]["AccountCurrencyCode"] = row.AccountCurrencyCode

        dtMonthKey = row.Date.replace(day=1)

        dAcctAggr[dtMonthKey]["Clicks"] += row.Clicks
        if row.ClickType in CLICKTYPES_TO_INCLUDE:
            dAcctAggr[dtMonthKey]["Impressions"] += row.Impressions
        dAcctAggr[dtMonthKey]["Cost"] += row.Cost
        dAcctAggr[dtMonthKey]["Conversions"] += row.Conversions
        dAcctAggr[dtMonthKey]["ViewThroughConversions"] += row.ViewThroughConversions
        dAcctAggr[dtMonthKey]["ConversionValue"] += row.TotalConvValue
        if row.ClickType in CLICKTYPES_TO_INCLUDE:
            dAcctAggr[dtMonthKey]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))
        
        # if row.AdNetworkType1 in [ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
        #     dTotal[row.AdNetworkType1]["Clicks"] += row.Clicks
        #     if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #         dTotal[row.AdNetworkType1]["Impressions"] += row.Impressions
        #     dTotal[row.AdNetworkType1]["Cost"] += row.Cost
        #     dTotal[row.AdNetworkType1]["Conversions"] += row.Conversions
        #     dTotal[row.AdNetworkType1]["ViewThroughConversions"] += row.ViewThroughConversions
        #     dTotal[row.AdNetworkType1]["ConversionValue"] += row.TotalConvValue
        #     dTotal[row.AdNetworkType1]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

        # dTotal['Total']["Clicks"] += row.Clicks
        # if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #     dTotal['Total']["Impressions"] += row.Impressions
        # dTotal['Total']["Cost"] += row.Cost
        # dTotal['Total']["Conversions"] += row.Conversions
        # dTotal['Total']["ViewThroughConversions"] += row.ViewThroughConversions
        # dTotal['Total']["ConversionValue"] += row.TotalConvValue
        # dTotal['Total']["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

        #if len(row.CampaignName) > iLongestName:
        #    iLongestName = len(row.CampaignName)


    


        # if dTotal['Total']["Impressions"] == 0:
        #     continue  #no results

    #return dAcctAggr

    oVSRows = models.VoiceStarCallLog.objects.filter(account_id__in=[x.ServiceAccountId for x in oVSs], call_s__gte=dtHistoricalStartMonth, call_s__lt=dtEnd, is_spam__exact=False) 

    oAGEmailRows = models.AGEmailLog.objects.filter(StoreNum__in=[x.InternalId for x in oVSs], ServerTime__gte=dtHistoricalStartMonth, ServerTime__lt=dtEnd) 

    #dDedupCalls[ServiceAccountId][call_s.date()][caller_number] += 1
    dStoreIdLookup = {}
    dDedupCalls = {}
    dDedupEmails = {}
    dAcctAggrByAccount = {}

    #setup
    for x in oVSs:
        dStoreIdLookup[x.InternalId] = x.ServiceAccountId
        dDedupCalls[x.ServiceAccountId] = collections.defaultdict(lambda: collections.defaultdict(int))
        dDedupEmails[x.ServiceAccountId] = collections.defaultdict(lambda: collections.defaultdict(int))
        dAcctAggrByAccount[x.ServiceAccountId] = collections.defaultdict(lambda: collections.defaultdict(int))

    

    #fill out dedup
    for row in oVSRows:
        dDedupCalls[row.account_id][row.call_s.date().replace(day=1)][row.caller_number] += 1
    for row in oAGEmailRows:
        dDedupEmails[dStoreIdLookup[row.StoreNum]][row.ServerTime.replace(day=1)][row.email] += 1


    #fill out aggr dicts
    for k, dd in dDedupCalls.iteritems():
        for sk, dNumbers in dd.iteritems():
            dtMonthKey = sk.replace(day=1)

            dAcctAggr[dtMonthKey]["Calls"] += len(dNumbers.keys()) #keys() is basically counting each number once
            dAcctAggrByAccount[k][dtMonthKey]['Calls'] += len(dNumbers.keys())

    for k, dd in dDedupEmails.iteritems():
        for sk, dEmails in dd.iteritems():
            dtMonthKey = sk.replace(day=1)

            dAcctAggr[dtMonthKey]["Emails"] += len(dEmails.keys()) #keys() is basically counting each number once
            dAcctAggrByAccount[k][dtMonthKey]['Emails'] += len(dEmails.keys())



    lsAGHistoricalLabels = [
        oGroup.Name,
        u"Impressions",
        u"Clicks", 
        u"CTR", 
        u"Avg. CPC", 
        u"Media",
        u"Total", 
        u"Calls",
        u"Emails",
        u"Contacts",
        u"Contact %",
        u"Cost/Contact"
    ]


    #book = Workbook()
    #campsheet = book.add_sheet(u'Overall Summary')
    ##kwsheet = book.add_sheet(u'Keyword Report')

    #campsheet.write(0,0,u'Campaign Report - %s (%s - %s)' % (sAcctName, lsDates[0].strftime(u"%b %d"), lsDates[-1].strftime(u"%b %d")), easyxf('font: name Calibri, bold true, height 220;'))
    for i, sName in enumerate(lsAGHistoricalLabels):
        sheet.write(0, i, sName, styleHeader)

    sheet.col(0).width = max(220 * iLongestName, 220 * 30)##256 * iLongestName
    for i, label in enumerate(lsAGHistoricalLabels):
        if not i == 0:
            sheet.col(i).width = 220 * max(15, len(label))
    
    i = 0  
    iYearBuf = 0

    for (id, d) in list(sorted(dAcctAggr.iteritems(), key=lambda x: x[0])):
        if d['Impressions'] > 0:
            if id.month == 1:
                sheet.write(i+1+iYearBuf, *[0, id.year, dCellStyles['bold_default']])
                iYearBuf += 1
            lsRowcols = _outputRowArgs(id, d)
            for col in lsRowcols:
                sheet.write(i+1+iYearBuf, *col)
            i += 1


    if len([x for x in oVSs if x.Active]) > 1:
        ##blank row
        i += 1
        i += 1
        sheet.write(i+1+iYearBuf, 0, oGroup.Name + " Contacts", styleHeader)
            

        i += 1
        lsSubtableLabels = ["Center","Sum of Call", "Sum of Email", " Sum of Contacts"]
        
        for j, lbl in enumerate(lsSubtableLabels):
            sheet.write(i+1+iYearBuf, j, lbl, styleHeader)

        i += 1



        #### breakout values here - TODO
        for oVS in oVSs:
            if oVS.Active:
                iCalls = dAcctAggrByAccount[oVS.ServiceAccountId][dtStartMonth.date()]["Calls"]
                iEmails = dAcctAggrByAccount[oVS.ServiceAccountId][dtStartMonth.date()]["Emails"]
                sheet.write(i+1+iYearBuf, 0, oVS.Name, dCellStyles["default"])
                sheet.write(i+1+iYearBuf, 1, unicode(iCalls), dCellStyles["default"])
                sheet.write(i+1+iYearBuf, 2, unicode(iEmails), dCellStyles["default"])
                sheet.write(i+1+iYearBuf, 3, unicode(iCalls + iEmails), dCellStyles["default"])
                i += 1


        
        ## simply use the last output (lsRowcols)
        sheet.write(i+1+iYearBuf, 0, "Grand Total", styleSubheader)
        sheet.write(i+1+iYearBuf, 1, lsRowcols[7][1], styleSubheader)
        sheet.write(i+1+iYearBuf, 2, lsRowcols[8][1], styleSubheader)
        sheet.write(i+1+iYearBuf, 3, lsRowcols[9][1], styleSubheader)
    
    
    return sheet


def Sheet_AG_Group_Acctv2(sheet, groupId, iMonth, iYear):  #, dAcctNameLookups={}
    def _outputRowArgs(k, d, bold=False):

        if d['Impressions']:
            CTR = float(d['Clicks'])/float(d['Impressions'])
        else:
            CTR = 0.0

        if d['Clicks']:
            avgCPC = float(d["Cost"])/float(d['Clicks'])
        else:
            avgCPC = 0.0

        if sum([x[1] for x in d["AvgPosAndClicks"]]) > 0:
            avgPos = "%.1f" % (sum([x[1] * x[0] for x in d["AvgPosAndClicks"]])/float(sum([x[1] for x in d["AvgPosAndClicks"]])))
        else:
            avgPos = "%.1f" % 0.0

        if d.has_key('Emails') and d['Emails']:
            costPerConv = float(d['Cost'])/float(d['Emails'])
        else:
            costPerConv = 0.0

        if d.has_key('Emails') and d['Emails'] and d['Clicks']:
            convRate = float(d['Emails'])/float(d['Clicks'])
        else:
            convRate = 0.0


        if d.has_key('ConversionValue') and d["ConversionValue"] and d['Cost']:
            convValueCost = float(d["ConversionValue"])/float(d["Cost"])
        else:
            convValueCost = 0.0


        if d['Clicks']:
            print float(d['Calls'] + d['Emails'])/float(d['Clicks'])
            contactPercent = float(d['Calls'] + d['Emails'])/float(d['Clicks'])
        else:
            contactPercent = 0.0

        if d.has_key('Emails') and d['Calls'] + d['Emails']:
            costPerContact = float(d['Cost'])*F_MARKUP/float(d['Calls'] + d['Emails'])
        else:
            costPerContact = 0.0

        if d['Cost']:
          fMarkedUpTotalCost = max(F_MIN_AMOUNT,float(d['Cost']) * F_MARKUP)
        else:
          fMarkedUpTotalCost = 0.0

        rowFormatted = [
            k.strftime("%b"),
            d['Impressions'], 
            d['Clicks'], 
           
            #"%.5f" % (float(d['Clicks'])/float(d['Impressions']),),
            CTR,
            #"%.2f" % avgCPC,
            avgCPC,
            d['Cost'],
            fMarkedUpTotalCost,
            d['Calls'],
            #avgPos,
            d['Emails'],
            d['Calls'] + d['Emails'],
            #"%.2f" % costPerConv,
            contactPercent,
            costPerContact
                   
        ]
        #print rowFormatted

        if bold:
            kExtra = "bold_"
        else:
            kExtra = ""

        rowcols = []
        #logging.warning(rowFormatted)
        for j, val in enumerate(rowFormatted):
            #logging.warning([i+2, j, val])
            if j in [4]:
                #print d 
                #rowcols.append([j, val, easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = CURRENCYCODE_TO_SYMBOL[d["AccountCurrencyCode"]]+'#,##0.00')])
                rowcols.append([j, val, dCellStyles[kExtra + "dollar"]])
            elif j in [5,6,11]:
                rowcols.append([j, val, dCellStyles[kExtra + "dollarwhole"]])
            elif j in [3,10]:
                rowcols.append([j, val, dCellStyles[kExtra + "percent"]])
            elif j in [1,2]:
                rowcols.append([j, val, dCellStyles[kExtra + "number"]])
            else:
                rowcols.append([j, val, dCellStyles[kExtra + "default"]])

        return rowcols

    
    styleHeader = easyxf(
        'font: name Calibri, colour white, height 220;'
        #'borders: left thick, right thick, top thick, bottom thick;'
        'pattern: pattern solid, fore_colour light_blue;',
        #num_format_str='YYYY-MM-DD'
    )

    styleSubheader = easyxf(
        'font: name Calibri, colour black, height 220;'
        #'borders: left thick, right thick, top thick, bottom thick;'
        'pattern: pattern solid, fore_colour pale_blue;',
        #num_format_str='YYYY-MM-DD'
    )



    dtStartMonth = datetime.datetime(month=iMonth, year=iYear, day=1, tzinfo=pytz.utc)
    dtEnd = dtStartMonth+dateutil.relativedelta.relativedelta(months=+1)
    dtHistoricalStartMonth = datetime.datetime(month=1, year=2011, day=1, tzinfo=pytz.utc)

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=dtHistoricalStartMonth, until=dtStartMonth):
        print dt.date()

    dAcctAggr = {}.fromkeys([dt.date() for dt in rrule.rrule(rrule.MONTHLY, dtstart=dtHistoricalStartMonth, until=dtStartMonth)])
    
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=dtHistoricalStartMonth, until=dtStartMonth):
        dAcctAggr[dt.date()] = {
                "AccountCurrencyCode":None,  #DEFAULT
                "Clicks":0,
                "Impressions":0,
                "Cost": 0,
                "AvgPosAndClicks":[],
                "Conversions":0,
                "ViewThroughConversions":0,
                "ConversionValue":0,
                "Calls":0,
                "Emails":0,

            }

    

    oGroup = models.AdAccountOwner.objects.get(id=groupId)
    oSubaccounts = [sa.subaccount for sa in oGroup.subaccounts.filter(subaccount__Active__exact=True)]

    if oGroup.InternalId:
        sGroupIds = oGroup.InternalId
    else:
        sGroupIds = ", ".join(sorted([sa.InternalId for sa in oSubaccounts]))


    dSubAccountsByInternalId = dict([(sa.InternalId, sa) for sa in [oGroup] + oSubaccounts])
    dAdAccountsByInternalId = collections.defaultdict(lambda: collections.defaultdict(list))
    dReverseVSIds = {}
    for sa in [oGroup] + oSubaccounts:
        dAdAccountsByInternalId[sa.InternalId][1] += [ac.AdAccount for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='1')]
        dAdAccountsByInternalId[sa.InternalId][2] += [ac.AdAccount for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='2')]
        for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='2'):
            dReverseVSIds[ac.AdAccount.ServiceAccountId] = sa.InternalId

    
    oGoogs = [ac.AdAccount for ac in oGroup.adaccounts.filter(AdAccount__ServiceType__exact='1', AdAccount__Active__exact=True)]
    oVSs = []
    for grp in [oGroup] + oSubaccounts:
       for ac in grp.adaccounts.filter(AdAccount__ServiceType__exact='2', AdAccount__Active__exact=True):
          oVSs.append(ac.AdAccount)

    
    iLenVSs = len(oVSs)

    oRows = models.GoogleAccountPerformanceReport.objects.filter(ExternalCustomerId__in=[x.ServiceAccountId for x in oGoogs], Date__gte=dtHistoricalStartMonth, Date__lt=dtEnd) 

    iLongestName = len("Campaign")

    # dTotal = {}
    # for groupvar in ['Total', ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
    #     dTotal[groupvar] = {
    #                 "CampaignName":ADNETWORKTYPE1_LABELS.get(groupvar, "Total"),
    #                 "Clicks":0,
    #                 "Impressions":0,
    #                 "Cost": 0,
    #                 "AvgPosAndClicks":[],
    #                 "Conversions":0,
    #                 "ViewThroughConversions":0,
    #                 "ConversionValue":0,
    #                 "AccountCurrencyCode":"USD"
    #            }

    for row in oRows:
        #if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #logging.warning([row.Date, row.CampaignName ])
        # if not dAcctAggr.has_key(row.CampaignId):
        #     dAcctAggr[row.CampaignId] = {
        #         "CampaignName":row.CampaignName,
        #         "AccountCurrencyCode":row.AccountCurrencyCode,  #DEFAULT
        #         "Clicks":0,
        #         "Impressions":0,
        #         "Cost": 0,
        #         "AvgPosAndClicks":[],
        #         "Conversions":0,
        #         "ViewThroughConversions":0,
        #         "ConversionValue":0
        #     }
        #     for subtotalkey in ["Total", ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
        #         dTotal[subtotalkey]["AccountCurrencyCode"] = row.AccountCurrencyCode

        dtMonthKey = row.Date.replace(day=1)

        dAcctAggr[dtMonthKey]["Clicks"] += row.Clicks
        if row.ClickType in CLICKTYPES_TO_INCLUDE:
            dAcctAggr[dtMonthKey]["Impressions"] += row.Impressions
        dAcctAggr[dtMonthKey]["Cost"] += row.Cost
        dAcctAggr[dtMonthKey]["Conversions"] += row.Conversions
        dAcctAggr[dtMonthKey]["ViewThroughConversions"] += row.ViewThroughConversions
        dAcctAggr[dtMonthKey]["ConversionValue"] += row.TotalConvValue
        if row.ClickType in CLICKTYPES_TO_INCLUDE:
            dAcctAggr[dtMonthKey]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))
        
        # if row.AdNetworkType1 in [ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
        #     dTotal[row.AdNetworkType1]["Clicks"] += row.Clicks
        #     if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #         dTotal[row.AdNetworkType1]["Impressions"] += row.Impressions
        #     dTotal[row.AdNetworkType1]["Cost"] += row.Cost
        #     dTotal[row.AdNetworkType1]["Conversions"] += row.Conversions
        #     dTotal[row.AdNetworkType1]["ViewThroughConversions"] += row.ViewThroughConversions
        #     dTotal[row.AdNetworkType1]["ConversionValue"] += row.TotalConvValue
        #     dTotal[row.AdNetworkType1]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

        # dTotal['Total']["Clicks"] += row.Clicks
        # if row.ClickType in CLICKTYPES_TO_INCLUDE:
        #     dTotal['Total']["Impressions"] += row.Impressions
        # dTotal['Total']["Cost"] += row.Cost
        # dTotal['Total']["Conversions"] += row.Conversions
        # dTotal['Total']["ViewThroughConversions"] += row.ViewThroughConversions
        # dTotal['Total']["ConversionValue"] += row.ConversionValue
        # dTotal['Total']["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

        #if len(row.CampaignName) > iLongestName:
        #    iLongestName = len(row.CampaignName)


    


        # if dTotal['Total']["Impressions"] == 0:
        #     continue  #no results

    #return dAcctAggr

    oVSRows = models.VoiceStarCallLog.objects.filter(account_id__in=[x.ServiceAccountId for x in oVSs], call_s__gte=dtHistoricalStartMonth, call_s__lt=dtEnd, is_spam__exact=False) 

    oAGEmailRows = models.AGEmailLog.objects.filter(StoreNum__in=dSubAccountsByInternalId.keys(), ServerTime__gte=dtHistoricalStartMonth, ServerTime__lt=dtEnd) 

    #dDedupCalls[ServiceAccountId][call_s.date()][caller_number] += 1
    dStoreIdLookup = {}
    dDedupCalls = {}
    dDedupEmails = {}
    dAcctAggrByAccount = {}

    #setup
    #for x in oVSs:
    for x in dSubAccountsByInternalId.iterkeys():
        #dStoreIdLookup[x.InternalId] = x.ServiceAccountId
        dDedupCalls[x] = collections.defaultdict(lambda: collections.defaultdict(int))
        dDedupEmails[x] = collections.defaultdict(lambda: collections.defaultdict(int))
        dAcctAggrByAccount[x] = collections.defaultdict(lambda: collections.defaultdict(int))

    

    #fill out dedup
    for row in oVSRows:
        dDedupCalls[dReverseVSIds[row.account_id]][row.call_s.date().replace(day=1)][row.caller_number] += 1
    for row in oAGEmailRows:
        dDedupEmails[row.StoreNum][row.ServerTime.replace(day=1)][row.email] += 1


    
    #fill out aggr dicts
    for k, dd in dDedupCalls.iteritems():
        for sk, dNumbers in dd.iteritems():
            dtMonthKey = sk.replace(day=1)

            dAcctAggr[dtMonthKey]["Calls"] += len(dNumbers.keys()) #keys() is basically counting each number once
            dAcctAggrByAccount[k][dtMonthKey]['Calls'] += len(dNumbers.keys())

    for k, dd in dDedupEmails.iteritems():
        for sk, dEmails in dd.iteritems():
            dtMonthKey = sk.replace(day=1)

            dAcctAggr[dtMonthKey]["Emails"] += len(dEmails.keys()) #keys() is basically counting each number once
            dAcctAggrByAccount[k][dtMonthKey]['Emails'] += len(dEmails.keys())

    print dAcctAggr[datetime.date(2014, 5, 1)]

    

    lsAGHistoricalLabels = [
        oGroup.Name + " (" + sGroupIds + ")",
        u"Impressions",
        u"Clicks", 
        u"CTR", 
        u"Avg. CPC", 
        u"Media",
        u"Total", 
        u"Calls",
        u"Emails",
        u"Contacts",
        u"Contact %",
        u"Cost/Contact"
    ]


    #book = Workbook()
    #campsheet = book.add_sheet(u'Overall Summary')
    ##kwsheet = book.add_sheet(u'Keyword Report')

    #campsheet.write(0,0,u'Campaign Report - %s (%s - %s)' % (sAcctName, lsDates[0].strftime(u"%b %d"), lsDates[-1].strftime(u"%b %d")), easyxf('font: name Calibri, bold true, height 220;'))
    for i, sName in enumerate(lsAGHistoricalLabels):
        sheet.write(0, i, sName, styleHeader)

    sheet.col(0).width = max(220 * iLongestName, 220 * 30)##256 * iLongestName
    for i, label in enumerate(lsAGHistoricalLabels):
        if not i == 0:
            sheet.col(i).width = 220 * max(15, len(label))
    
    i = 0  
    iYearBuf = 0

    iLastYear = 0
    for (id, d) in list(sorted(dAcctAggr.iteritems(), key=lambda x: x[0])):

        if d['Impressions'] > 0 or d['Calls'] > 0 or d['Emails'] > 0:
            if id.month == 1 or iLastYear != id.year:
                sheet.write(i+1+iYearBuf, *[0, id.year, dCellStyles['bold_default']])
                iYearBuf += 1
            lsRowcols = _outputRowArgs(id, d)
            for col in lsRowcols:
                sheet.write(i+1+iYearBuf, *col)
            i += 1
            iLastYear = id.year


    if len([x for x in oVSs if x.Active]) > 1:
        ##blank row
        i += 1
        i += 1
        sheet.write(i+1+iYearBuf, 0, oGroup.Name + " Contacts", styleHeader)
            

        i += 1
        lsSubtableLabels = ["Center","Sum of Call", "Sum of Email", " Sum of Contacts"]
        
        for j, lbl in enumerate(lsSubtableLabels):
            sheet.write(i+1+iYearBuf, j, lbl, styleHeader)

        i += 1



        #### breakout values here - TODO
        #for oVS in oVSs:
        for iid, sa in dSubAccountsByInternalId.iteritems():
            if sa.id != oGroup.id:
                #if oVS.Active:
                iCalls = dAcctAggrByAccount[iid][dtStartMonth.date()]["Calls"]
                iEmails = dAcctAggrByAccount[iid][dtStartMonth.date()]["Emails"]
                sheet.write(i+1+iYearBuf, 0, sa.Name + " (" + sa.InternalId + ")", dCellStyles["default"])
                sheet.write(i+1+iYearBuf, 1, unicode(iCalls), dCellStyles["default"])
                sheet.write(i+1+iYearBuf, 2, unicode(iEmails), dCellStyles["default"])
                sheet.write(i+1+iYearBuf, 3, unicode(iCalls + iEmails), dCellStyles["default"])
                i += 1


        
        ## simply use the last output (lsRowcols)
        sheet.write(i+1+iYearBuf, 0, "Grand Total", styleSubheader)
        sheet.write(i+1+iYearBuf, 1, lsRowcols[7][1], styleSubheader)
        sheet.write(i+1+iYearBuf, 2, lsRowcols[8][1], styleSubheader)
        sheet.write(i+1+iYearBuf, 3, lsRowcols[9][1], styleSubheader)
    
    
    return sheet

import calendar
def dumpAGXL(groupId, iMonth, iYear,timestamp=datetime.datetime.now(pytz.utc)):
    iWeekdayOfFirst, iDaysInMonth = calendar.monthrange(iYear,iMonth)
    sMonthAbbr = calendar.month_abbr[iMonth]
    oGroup = models.Group.objects.get(id=groupId)
    book = Workbook()
    acctsheet = book.add_sheet(u'Overall Summary')
    kwsheet = book.add_sheet(u'Keyword Report %s 1 - %i' % (sMonthAbbr, iDaysInMonth))
    
    kwsheet = Sheet_AG_Group_KW(kwsheet, groupId, iMonth, iYear)
    acctsheet = Sheet_AG_Group_Acct(acctsheet, groupId, iMonth, iYear)
    #book.save(REPORT_DUMP_PATH + '%s_%s_%s.xls' % (timestamp.strftime("%Y%m%d"), oGroup.MasterAccount.Name, oGroup.Name))
    book.save('/home/ubuntu/' + '%s%02d_%s_%s_v%s.xls' % (unicode(iYear), iMonth, oGroup.MasterAccount.Name.replace("/", "-"), oGroup.Name.replace("/", "-"), timestamp.strftime("%Y%m%d"), ))
    
def dumpAGXLv2(groupId, iMonth, iYear,reportName=None,timestamp=datetime.datetime.now(pytz.utc)):
    oGroup = models.AdAccountOwner.objects.get(id=groupId)
    oSubaccounts = [sa.subaccount for sa in oGroup.subaccounts.filter(subaccount__Active__exact=True)]

    if oGroup.InternalId:
        sGroupIds = oGroup.InternalId
    else:
        sGroupIds = ", ".join(sorted([sa.InternalId for sa in oSubaccounts]))

    if not reportName:
        reportName = oGroup.MasterAccount.Name.replace("/", "-") + "_" + oGroup.Name.replace("/", "-") + "_" + sGroupIds.replace(", ", "+")
    iWeekdayOfFirst, iDaysInMonth = calendar.monthrange(iYear,iMonth)
    sMonthAbbr = calendar.month_abbr[iMonth]
    
    book = Workbook()
    acctsheet = book.add_sheet(u'Overall Summary')
    kwsheet = book.add_sheet(u'Keyword Report %s 1 - %i' % (sMonthAbbr, iDaysInMonth))
    
    kwsheet = Sheet_AG_Group_KWv2(kwsheet, groupId, iMonth, iYear)
    acctsheet = Sheet_AG_Group_Acctv2(acctsheet, groupId, iMonth, iYear)
    #book.save(REPORT_DUMP_PATH + '%s_%s_%s.xls' % (timestamp.strftime("%Y%m%d"), oGroup.MasterAccount.Name, oGroup.Name))
    #book.save('/home/ubuntu/' + '%s%02d_%s_%s_v%s.xls' % (unicode(iYear), iMonth, oGroup.MasterAccount.Name.replace("/", "-"), oGroup.Name.replace("/", "-"), timestamp.strftime("%Y%m%d"), ))
    #book.save(REPORT_DUMP_PATH + '%s_%s_%s.xls' % (timestamp.strftime("%Y%m%d"), reportName, sAcctName,)
    logging.warning(groupId)
    logging.warning(reportName)
    book.save(REPORT_DUMP_PATH + '%s%02d_%s_v%s.xls' % (unicode(iYear), iMonth, reportName, timestamp.strftime("%Y%m%d"), ))

# def generateAllAGReports(iMonth, iYear):
#     grps2 = models.Group.objects.filter(MasterAccount__exact=2, account__Active__exact=True).distinct()
#     for g in grps2:                                                                          
#        dumpAGXL(g.id, iMonth, iYear)



def generateAllAGReportsv2(iMonth, iYear):
    grps2 = models.AdAccountOwner.objects.filter(MasterAccount__exact=2, parental__isnull=True, Active__exact=True)  #top level account owners
    for g in grps2:                                                                          
       dumpAGXLv2(g.id, iMonth, iYear)



def dumpToXl(lsCustIds, lsSDates, reportName, timestamp=datetime.datetime.now(pytz.utc), format="campaign"):  #, dAcctNameLookups={}
    def _outputRowArgs(d, bold=False):

        if d['Impressions']:
            CTR = float(d['Clicks'])/float(d['Impressions'])
        else:
            CTR = 0.0

        if d['Clicks']:
            avgCPC = float(d["Cost"])/float(d['Clicks'])
        else:
            avgCPC = 0.0

        if sum([x[1] for x in d["AvgPosAndClicks"]]) > 0:
            avgPos = "%.1f" % (sum([x[1] * x[0] for x in d["AvgPosAndClicks"]])/float(sum([x[1] for x in d["AvgPosAndClicks"]])))
        else:
            avgPos = "%.1f" % 0.0

        if d['Conversions']:
            costPerConv = float(d['Cost'])/float(d['Conversions'])
        else:
            costPerConv = 0.0

        if d['Clicks']:
            convRate = float(d['Conversions'])/float(d['Clicks'])
        else:
            convRate = 0.0


        if d['Cost']:
            convValueCost = float(d["ConversionValue"])/float(d["Cost"])
        else:
            convValueCost = 0.0



        rowFormatted = [
            d['CampaignName'], 
            d['Clicks'], 
            d['Impressions'], 
            #"%.5f" % (float(d['Clicks'])/float(d['Impressions']),),
            CTR,
            #"%.2f" % avgCPC,
            avgCPC,
            d['Cost'],
            avgPos,
            #avgPos,
            d['Conversions'],
            #"%.2f" % costPerConv,
            costPerConv,
            #"%.2f" % convRate,
            convRate,
            d["ViewThroughConversions"],
            d["ConversionValue"],
            "%.2f" % convValueCost,
            #"NA",
            #"NA",
            #"NA",
            #d["ConversionValue"]       
        ]
        #print rowFormatted

        if bold:
            fontExtra = ", bold true"
        else:
            fontExtra = ""

        rowcols = []
        for j, val in enumerate(rowFormatted):
            #logging.warning([i+2, j, val])
            if j in [4,5,8,11,12,16]:
                #print d 
                #rowcols.append([j, val, easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = CURRENCYCODE_TO_SYMBOL[d["AccountCurrencyCode"]]+'#,##0.00')])
                rowcols.append([j, val, easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = '$#,##0.00')])
            elif j in [3,9]:
                rowcols.append([j, val, easyxf('font: name Calibri, height 220%s;' % fontExtra,num_format_str = '0.00%')])
            else:
                rowcols.append([j, val, easyxf('font: name Calibri, height 220%s;' % fontExtra)])

        return rowcols

    

    camplabels = [
        u"Campaign",
        u"Clicks", 
        u"Impressions",
        u"CTR", 
        u"Avg. CPC", 
        u"Cost", 
        u"Avg. position", 
        u"Bookings", 
        u"Cost / Booking", 
        u"Conv Rate",
        u"View-through conv.", 
        u"Booking value",
        u"Booking value / cost",
        #u"Phone impressions",
        #u"Phone calls",
        #u"Phone costs",
        #u"Total costs"
    ]

    styleHeader = easyxf(
        'font: name Calibri, colour white, height 220;'
        #'borders: left thick, right thick, top thick, bottom thick;'
        'pattern: pattern solid, fore_colour light_blue;',
        #num_format_str='YYYY-MM-DD'
    )



    lsDates = [dateutil.parser.parse(date) for date in lsSDates]

    for sCustId in lsCustIds:
        sAcctName = models.mongodb.reports.find_one({'customerId':sCustId})['name'].replace("/", "_")
        #sAcctName = dAcctNameLookups[sCustId]['name']
        logging.warning([sCustId, [lsDates[0].date().isoformat(), lsDates[-1].date().isoformat()]])



        dCampaignAggr = {}
        oRows = models.GoogleCampaignPerformanceReport.objects.filter(ExternalCustomerId__exact=sCustId, Date__range=[lsDates[0].date().isoformat(), lsDates[-1].date().isoformat()])
        iLongestName = len("Campaign")

        dTotal = {}
        for groupvar in ['Total', ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
            dTotal[groupvar] = {
                        "CampaignName":ADNETWORKTYPE1_LABELS.get(groupvar, "Total"),
                        "Clicks":0,
                        "Impressions":0,
                        "Cost": 0,
                        "AvgPosAndClicks":[],
                        "Conversions":0,
                        "ViewThroughConversions":0,
                        "ConversionValue":0,
                        "AccountCurrencyCode":"USD"
                    }

        for row in oRows:
            #if row.ClickType in CLICKTYPES_TO_INCLUDE:
            #logging.warning([row.Date, row.CampaignName ])
            if not dCampaignAggr.has_key(row.CampaignId):
                dCampaignAggr[row.CampaignId] = {
                    "CampaignName":row.CampaignName,
                    "AccountCurrencyCode":row.AccountCurrencyCode,  #DEFAULT
                    "Clicks":0,
                    "Impressions":0,
                    "Cost": 0,
                    "AvgPosAndClicks":[],
                    "Conversions":0,
                    "ViewThroughConversions":0,
                    "ConversionValue":0
                }
                for subtotalkey in ["Total", ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
                    dTotal[subtotalkey]["AccountCurrencyCode"] = row.AccountCurrencyCode


            dCampaignAggr[row.CampaignId]["Clicks"] += row.Clicks
            if row.ClickType in CLICKTYPES_TO_INCLUDE:
                dCampaignAggr[row.CampaignId]["Impressions"] += row.Impressions
            dCampaignAggr[row.CampaignId]["Cost"] += row.Cost
            dCampaignAggr[row.CampaignId]["Conversions"] += row.Conversions
            dCampaignAggr[row.CampaignId]["ViewThroughConversions"] += row.ViewThroughConversions
            dCampaignAggr[row.CampaignId]["ConversionValue"] += row.TotalConvValue
            dCampaignAggr[row.CampaignId]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))
            
            if row.AdNetworkType1 in [ADNETWORKTYPE1_DISPLAY_NETWORK_KEY, ADNETWORKTYPE1_SEARCH_NETWORK_KEY]:
                dTotal[row.AdNetworkType1]["Clicks"] += row.Clicks
                if row.ClickType in CLICKTYPES_TO_INCLUDE:
                    dTotal[row.AdNetworkType1]["Impressions"] += row.Impressions
                dTotal[row.AdNetworkType1]["Cost"] += row.Cost
                dTotal[row.AdNetworkType1]["Conversions"] += row.Conversions
                dTotal[row.AdNetworkType1]["ViewThroughConversions"] += row.ViewThroughConversions
                dTotal[row.AdNetworkType1]["ConversionValue"] += row.TotalConvValue
                dTotal[row.AdNetworkType1]["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

            dTotal['Total']["Clicks"] += row.Clicks
            if row.ClickType in CLICKTYPES_TO_INCLUDE:
                dTotal['Total']["Impressions"] += row.Impressions
            dTotal['Total']["Cost"] += row.Cost
            dTotal['Total']["Conversions"] += row.Conversions
            dTotal['Total']["ViewThroughConversions"] += row.ViewThroughConversions
            dTotal['Total']["ConversionValue"] += row.TotalConvValue
            dTotal['Total']["AvgPosAndClicks"].append((row.AveragePosition, row.Impressions))

            if len(row.CampaignName) > iLongestName:
                iLongestName = len(row.CampaignName)


        if dTotal['Total']["Impressions"] == 0:
            continue  #no results

        book = Workbook()
        campsheet = book.add_sheet(u'Campaign Report')
        ##kwsheet = book.add_sheet(u'Keyword Report')

        campsheet.write(0,0,u'Campaign Report - %s (%s - %s)' % (sAcctName, lsDates[0].strftime(u"%b %d"), lsDates[-1].strftime(u"%b %d")), easyxf('font: name Calibri, bold true, height 220;'))
        for i, sName in enumerate(camplabels):
            campsheet.write(1, i, sName, styleHeader)

        campsheet.col(0).width = max(220 * iLongestName, 220 * 30)##256 * iLongestName
        for i, label in enumerate(camplabels):
            if not i == 0:
                campsheet.col(i).width = 220 * max(15, len(label))
        
        i = 0  #just in case there are not items
        for i, (id, d) in enumerate(list(sorted(dCampaignAggr.iteritems(), key=lambda x: x[1]['CampaignName']))):
            lsRowcols = _outputRowArgs(d)
            for col in lsRowcols:
                campsheet.write(i+2, *col)

        ##blank row
        i += 1
        i += 1
          

        for subtotalkey in [ADNETWORKTYPE1_SEARCH_NETWORK_KEY, ADNETWORKTYPE1_DISPLAY_NETWORK_KEY]:
            if dTotal[subtotalkey]['Impressions'] > 0:
                lsRowcols = _outputRowArgs(dTotal[subtotalkey])
                for col in lsRowcols:
                    campsheet.write(i+2, *col)
                i += 1
                
        lsRowcols = _outputRowArgs(dTotal['Total'], bold=True)
        for col in lsRowcols:
            campsheet.write(i+2, *col)


        
        book.save(REPORT_DUMP_PATH + '%s_%s_%s.xls' % (timestamp.strftime("%Y%m%d"), reportName, sAcctName,))



import datetime, pytz
from dateutil import relativedelta
from main import models
from django.db import connection


TODAY = datetime.date.today()



sSQLCleanDaily = """
BEGIN;
DROP TABLE IF EXISTS updatr_daily;
CREATE TABLE updatr_daily
(
  masteraccount_id bigint NOT NULL,
  masteraccount_name character varying(200) NOT NULL, 
  group_id bigint NOT NULL,
  group_name character varying(200) NOT NULL,
  date date NOT NULL,
  cost numeric(16,2),
  total_cost numeric(16,2),
  "GoogleId" bigint,
  calls bigint,
  emails bigint,
  week double precision,
  month double precision,
  year double precision,
  name character varying(200),
  state_code character varying(10),
  impressions integer,
  clicks integer, 
  avg_position double precision,
  dma  character varying(300),
  internalid character varying(80)

)
WITH (
  OIDS=FALSE
);
ALTER TABLE updatr_daily
  OWNER TO lars;
GRANT ALL ON TABLE updatr_daily TO lars;
GRANT SELECT ON TABLE updatr_daily TO reader;
COMMIT;
"""


sSQLExisting = """
SELECT masteraccount_id, group_id, date from updatr_daily;
"""

sSQLAddDaily = """
INSERT INTO updatr_daily (masteraccount_id, masteraccount_name, group_id, group_name, date, cost, total_cost, "GoogleId", calls, emails, week, month, year, name, impressions, clicks, avg_position, internalid)
VALUES (%(masteraccount_id)s, '%(masteraccount_name)s', %(group_id)s, '%(group_name)s', '%(date)s', %(cost)s, %(total_cost)s, %(GoogleId)s, %(calls)s, %(conversions)s, %(week)s, %(month)s, %(year)s, '%(name)s', %(impressions)s, %(clicks)s, %(avg_position)s, '%(internalid)s');
"""

sSQLUpdateDaily = """
UPDATE updatr_daily SET (masteraccount_id, masteraccount_name, group_id, group_name, date, cost, total_cost, "GoogleId", calls, emails, week, month, year, name, impressions, clicks, avg_position, internalid)
= (%(masteraccount_id)s, '%(masteraccount_name)s', %(group_id)s, '%(group_name)s', '%(date)s', %(cost)s, %(total_cost)s, %(GoogleId)s, %(calls)s, %(conversions)s, %(week)s, %(month)s, %(year)s, '%(name)s', %(impressions)s, %(clicks)s, %(avg_position)s, '%(internalid)s')
WHERE masteraccount_id = %(masteraccount_id)s
  AND group_id = %(group_id)s
  AND date = '%(date)s';
;
"""

import itertools

class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

def loadDataTables(days_back=7, update=True, reset=False, aaos=None, test=False):
    dates = []
    if not aaos: aaos = []

    for i in xrange(days_back):
    #for i in xrange(7):

        ## starts with yesterday since today is not finished
        dates.append((TODAY + relativedelta.relativedelta(days=-i-1)))



    cursor = connection.cursor()

    print 'ere'
    if reset:
        if not test:
            cursor.execute(sSQLCleanDaily)

    dPseudoKeys = {}
    print 'ere'

    if not reset:

        cursor.execute(sSQLExisting)
        
        print 'ere'
        column_names = [d[0] for d in cursor.description]
        
        lsExiting = [Row(itertools.izip(column_names, row)) for row in cursor]
        print 'ere'
        for d in lsExiting:
            dPseudoKeys[unicode(d['masteraccount_id']) + "_" + unicode(d['group_id']) + "_" + unicode(d['date'].isoformat())] = True
    
    print "Processing dates now"


    lsValidMasterIds = [oMaster.id for oMaster in models.MasterAccount.objects.all() if oMaster.GoogleMCCId]
  



    if aaos:
        oSelectTopGroups = models.AdAccountOwner.objects.filter(MasterAccount__in=lsValidMasterIds, parental__isnull=True, id__in=aaos)
    else:
        oSelectTopGroups = models.AdAccountOwner.objects.filter(MasterAccount__in=lsValidMasterIds, parental__isnull=True)

    print oSelectTopGroups

    for oGroup in oSelectTopGroups:  #top level account owners
        print oGroup
        oSubaccounts = [sa.subaccount for sa in oGroup.subaccounts.all()]

        dSubAccountsByInternalId = dict([(sa.InternalId, sa) for sa in [oGroup] + oSubaccounts])
        dAdAccountsByInternalId = collections.defaultdict(lambda: collections.defaultdict(list))
        dReverseVSIds = {}
        for sa in [oGroup] + oSubaccounts:
            dAdAccountsByInternalId[sa.InternalId][1] += [ac.AdAccount for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='1')]
            dAdAccountsByInternalId[sa.InternalId][2] += [ac.AdAccount for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='2')]
            for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='2'):
                dReverseVSIds[ac.AdAccount.ServiceAccountId] = sa.InternalId


    #for lc in models.Group.objects.all():

        # googCAs = lc.account_set.filter(ServiceType__exact="1")
        # if googCAs:
        #     googId = googCAs[0].ServiceAccountId
        # else:
        #     googId = 'NULL'
        # oVSs = lc.account_set.filter(ServiceType__exact="2")
        # vsIds = [x.ServiceAccountId for x in oVSs]
        # #if oVSs:
        # #    vsId = vsCAs[0].ServiceAccountId

        googIds, vsIds, oVSs = [], [], []
        for sa in [oGroup] + oSubaccounts:
            googIds += [ac.AdAccount.ServiceAccountId for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='1')]
            vsIds += [ac.AdAccount.ServiceAccountId for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='2')]
            oVSs += [ac.AdAccount for ac in sa.adaccounts.filter(AdAccount__ServiceType__exact='2')]

        ### we dedup by month so we need to injest the relevant months, sometimes more than one
        startMonth = sorted(dates)[0].replace(day=1)

        endMonthFrom = sorted(dates)[-1]
        wd, iNumDaysInMonth = calendar.monthrange(endMonthFrom.year, endMonthFrom.month)
        endMonth = endMonthFrom.replace(day=iNumDaysInMonth)

        #VS uses datetimes, not dates so we need to add on second before midnight to the endMonth
        endMonthTime = datetime.datetime.combine(endMonth, datetime.datetime.max.time())  # appends 23:59:59.999999

        print startMonth
        print endMonth, endMonthTime

        oVSRows = models.VoiceStarCallLog.objects.filter(account_id__in=vsIds, call_s__gte=startMonth, call_s__lte=endMonthTime, is_spam__exact=False).order_by('call_s')

        print ""
        if oGroup.MasterAccount.id == 2: 
            oAGEmailRows = models.AGEmailLog.objects.filter(StoreNum__in=[x.upper() for x in dSubAccountsByInternalId.keys()], ServerTime__gte=startMonth, ServerTime__lte=endMonth).order_by('ServerTime')

        #dDedupCalls[ServiceAccountId][call_s.date()][caller_number] += 1
        dStoreIdLookup = {}
        dDedupCalls = {}
        dDedupEmails = {}
        dAcctAggrByAccount = {}

        dFirstCalled = {}
        dFirstEmailed = {}



        #setup
        #for x in oVSs:
        for x in dSubAccountsByInternalId.iterkeys():
            #dStoreIdLookup[dReverseVSIds[x.ServiceAccountId]] = x.ServiceAccountId
            dDedupCalls[x] = collections.defaultdict(lambda: collections.defaultdict(int))
            dDedupEmails[x] = collections.defaultdict(lambda: collections.defaultdict(int))
            dAcctAggrByAccount[x] = collections.defaultdict(lambda: collections.defaultdict(int))
            dFirstCalled[x] = collections.defaultdict(dict)
            dFirstEmailed[x] = collections.defaultdict(dict)

        

        # #fill out dedup
        # for row in oVSRows:
        #     dDedupCalls[dReverseVSIds[row.account_id]][row.call_s.date().replace(day=1)][row.caller_number] += 1
        # for row in oAGEmailRows:
        #     dDedupEmails[row.StoreNum][row.ServerTime.replace(day=1)][row.email] += 1
            

        #fill out dedup
        for row in oVSRows:
            #print "CALL", row, dReverseVSIds[row.account_id], row.call_s.date(), row.caller_number
            if not row.caller_number in dFirstCalled[dReverseVSIds[row.account_id]][row.call_s.date().replace(day=1)].iterkeys():
                dFirstCalled[dReverseVSIds[row.account_id]][row.call_s.date().replace(day=1)][row.caller_number] = row.call_s
                dDedupCalls[dReverseVSIds[row.account_id]][row.call_s.date()][row.caller_number] += 1
                #print "+++", dReverseVSIds[row.account_id], row.call_s.date(), row.caller_number
        if oGroup.MasterAccount.id == 2:     
            for row in oAGEmailRows:
                #print "EMAIL", row
                if not row.email in dFirstEmailed[row.StoreNum][row.ServerTime.replace(day=1)].iterkeys():
                    dFirstEmailed[row.StoreNum][row.ServerTime.replace(day=1)][row.email] = row.ServerTime
                    dDedupEmails[row.StoreNum][row.ServerTime][row.email] += 1
                    #print "+++", row.StoreNum, row.ServerTime, row.email


        # #fill out aggr dicts
        # for k, dd in dDedupCalls.iteritems():
        #     for sk, dNumbers in dd.iteritems():
        #         dtMonthKey = sk.replace(day=1)

        #         dAcctAggr[dtMonthKey]["Calls"] += len(dNumbers.keys()) #keys() is basically counting each number once
        #         dAcctAggrByAccount[k][dtMonthKey]['Calls'] += len(dNumbers.keys())

        # for k, dd in dDedupEmails.iteritems():
        #     for sk, dEmails in dd.iteritems():
        #         dtMonthKey = sk.replace(day=1)

        #         dAcctAggr[dtMonthKey]["Emails"] += len(dEmails.keys()) #keys() is basically counting each number once
        #         dAcctAggrByAccount[k][dtMonthKey]['Emails'] += len(dEmails.keys())


 



        if not test:
            cursor.execute("BEGIN;")

        for date in dates:

            sThisPseudoKey = unicode(oGroup.MasterAccount.id) + "_" + unicode(oGroup.id) + "_" + unicode(date.isoformat())
            if not dPseudoKeys.has_key(sThisPseudoKey) or update:


                dRow = {}
                
            
                try:
                    if googIds: #!= "NULL":
                        googs = models.GoogleAccountPerformanceReport.objects.filter(ExternalCustomerId__in=googIds, Date__exact=date  )
                        googsCampaign = models.GoogleCampaignPerformanceReport.objects.filter(ExternalCustomerId__in=googIds, Date__exact=date  )
                    else:
                        googs = []
                        googsCampaign = []
                    

                    



                    print oGroup.Name
                    #print googs
                    #print calls
                    dRow['masteraccount_id'] = oGroup.MasterAccount.id
                    dRow['group_id'] = oGroup.id
                    dRow['internalid'] = oGroup.InternalId
                    dRow['masteraccount_name'] = oGroup.MasterAccount.Name
                    dRow['group_name'] = oGroup.Name
                    dRow['date'] = date
                    dRow['cost'] = 0.00
                    dRow['impressions'] = 0
                    dRow['clicks'] = 0
                    if oGroup.MasterAccount.id == 2: ###AlphaGraphics should use the AGEmailLog as is more accurate

                        iEmails = 0
                        for sa in [oGroup] + oSubaccounts:
                        #for vsId in vsIds:
                            #print "EMAIL PREADD", date, sa.InternalId, dDedupEmails.has_key(sa.InternalId), dDedupEmails[sa.InternalId].has_key(date), dDedupEmails[sa.InternalId][date].keys()
                            if dDedupEmails.has_key(sa.InternalId) and dDedupEmails[sa.InternalId].has_key(date):
                                iEmails += len(dDedupEmails[sa.InternalId][date].keys())
                        
                        dRow['conversions'] = iEmails

                    else:
                        dRow['conversions'] = sum([goog.Conversions for goog in googsCampaign])
                    
                    for goog in googs:
                        dRow['cost'] += float(goog.Cost)
                        if goog.ClickType in CLICKTYPES_TO_INCLUDE:
                            dRow['impressions'] += goog.Impressions
                        dRow['clicks'] += goog.Clicks
                    
                    fDenom = sum([goog.Impressions for goog in googs if goog.ClickType in CLICKTYPES_TO_INCLUDE])
                    if googs and fDenom:
                        dRow['avg_position'] = sum([goog.Impressions * goog.AveragePosition for goog in googs if goog.ClickType in CLICKTYPES_TO_INCLUDE])/fDenom

                    else:
                        dRow['avg_position'] = 'NULL'

                    if dRow['cost']:
                      fMarkedUpTotalCost = max(F_MIN_AMOUNT,float(dRow['cost']) * F_MARKUP)
                    else:
                      fMarkedUpTotalCost = 0.0

                    dRow['total_cost'] = fMarkedUpTotalCost
                    
                    if googIds:
                        dRow['GoogleId'] = googIds[0]
                    else:
                        dRow['GoogleId'] = 'NULL'

                    iCalls = 0
                    #for vsId in vsIds:
                    for sa in [oGroup] + oSubaccounts:
                        if dDedupCalls.has_key(sa.InternalId) and dDedupCalls[sa.InternalId].has_key(date):
                            iCalls += len(dDedupCalls[sa.InternalId][date].keys()) 
                    dRow['calls'] = iCalls
                    dRow['week'] = date.isocalendar()[1]
                    dRow['month'] = date.month
                    dRow['year'] = date.year
                    dRow['name'] = oGroup.Name

                    ## these are account level
                    #dRow['state_code']
                    #dRow['dma'] = 
                    print dRow

                      
                except models.GoogleAccountPerformanceReport.DoesNotExist:
                    print "Does not exist"
                    continue


                for k in ['name', 'group_name']:
                    dRow[k] = dRow[k].replace("%", "%%").replace(r"'", r"''")

                

                if not dPseudoKeys.has_key(sThisPseudoKey):
                    print sSQLAddDaily % dRow
                    if not test:
                        cursor.execute(sSQLAddDaily % dRow, {})
                    
                else:
                    print sSQLUpdateDaily % dRow
                    if not test:
                        cursor.execute(sSQLUpdateDaily % dRow, {})
                    
        if not test:
            cursor.execute("COMMIT;")







lsCustIds = None
def test(b=None,c=None):
    if not b or not c:
        a,b,c = getAccounts()
    sAllIds = set(b.keys())
    sMgrIds = set(c.keys())
    sEndNodeIds = sAllIds.difference(sMgrIds)
    lsCustIds = list(sEndNodeIds) #[:10]
    print lsCustIds
    #dlAccountPerf(lsCustIds)
    #dlCampaignPerf(lsCustIds)
    #dlKeywordPerf(lsCustIds)
    #dlGeoPerf(lsCustIds)


    # for id in lsCustIds:
    #     logging.info("CSV dump of custid %s" % id)
    #     loadCSV(id, None)


#### Where we left off, 
# """
# trying to figure out how to do a rollup report.  
# Can get individual low-level account by account.  May need to just redo client for every low level client.
# Use the CustomerService code to get all the customer ids




#loading kws to db, next do geos 
#fill in rest of geos to complete Jan

# """




