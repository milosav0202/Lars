#-*- coding:utf-8 -*-
import sys, os, logging
PROJECT_ROOT = os.path.abspath( 
    os.path.dirname(__file__) + "../" 
)

sys.path = [PROJECT_ROOT] + sys.path
    

from django.core.management import setup_environ
from lars import settings
setup_environ(settings)

import httplib2, time, csv
from dateutil import parser
from django.db import transaction
from apiclient.discovery import build
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsReportError

from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError, SignedJwtAssertionCredentials

from main import models



loggr = logging.getLogger("")
loggr.setLevel(logging.INFO)

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
    client = AdWordsClient(path='~/', headers={
        'clientCustomerId': '433-908-0283', #Lars MCC

        #'clientCustomerId': '990-671-7951', #SANDBOX ACCT
        #'clientCustomerId':'450-614-3003',
        #'clientCustomerId':'9663107432',
     'developerToken': 'KuxisPFnqHFfkJetsOyMGQ',
     'email': 'larsmarketing@arborheights.net',
     'password': 'babal000',
     'userAgent': 'Lars',
     'debug': 'y',
     'home': '/home/ubuntu',
     'log_home': '/home/ubuntu/logs',
     'request_log': 'y',
     'xml_log': 'y',
     'xml_parser': '1'})
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
    print '%s%s, %s, %s' % (prefix, account['login'], account['customerId'],
                          account['name'])
    if account['customerId'] in links:
        for child_link in links[account['customerId']]:
            child_account = accounts[child_link['clientCustomerId']]
            DisplayAccountTree(child_account, child_link, accounts, links, depth + 1)




def getAccounts(showTree=False):
    #Initialize appropriate service.
    client = getClient()
    managed_customer_service = client.GetManagedCustomerService(
      'https://adwords.google.com', 'v201209')

    # Construct selector to get all accounts.
    selector = {
      'fields': ['Login', 'CustomerId', 'Name']
    }
    # Get serviced account graph.
    graph = managed_customer_service.Get(selector)[0]
    if 'entries' in graph and graph['entries']:
        # Create map from customerId to parent and child links.
        child_links = {}
        parent_links = {}
        if 'links' in graph:
            for link in graph['links']:
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
            accounts[account['customerId']] = account
            if account['customerId'] not in parent_links:
                root_account = account
        # Display account tree.
        if root_account:
            if showTree:
                print 'Login, CustomerId, Name'
                DisplayAccountTree(root_account, None, accounts, child_links, 0)
        else:
            print 'Unable to determine a root account'
    else:
        print 'No serviced accounts were found'

    print
    print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                             client.GetOperations()))


    return root_account, accounts, child_links




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



def dlAccountPerf(lsCustIds):
    client = getClient()
    #dlr = client.GetReportDownloader('https://adwords.google.com', 'v201209')
    dlrreport = {                     
          #'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
          'reportName':'ACCOUNT_PERFORMANCE_REPORT',
          #'dateRangeType': 'LAST_7_DAYS',
          #'dateRangeType': 'LAST_30_DAYS',
          'dateRangeType': 'CUSTOM_DATE',
          
          'reportType': 'ACCOUNT_PERFORMANCE_REPORT',
          'downloadFormat': 'CSV',
          'selector': {
              'fields': ['AccountDescriptiveName', 'Date', 'AccountCurrencyCode', 'AccountId','AccountTimeZoneId',
                            'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition','ExternalCustomerId'],
              'dateRange':['20130101', '20130121']
          },
          # Enable to get rows with zero impressions.
          'includeZeroImpressions': 'false'
      }

    for sCustId in lsCustIds:
        
        print "Downloading custid", sCustId
        logging.info("Downloading custid %s" % sCustId)
        client.SetClientCustomerId(sCustId)
        dlr = client.GetReportDownloader('https://adwords.google.com', 'v201209')
        file_path = dlr.DownloadReport(dlrreport, file_path='/home/ubuntu/dlreports/googAcctPerf_' + sCustId + '_Latest.csv')


def dlCampaignPerf(lsCustIds):
    client = getClient()
    #dlr = client.GetReportDownloader('https://adwords.google.com', 'v201209')
    dlrreport = {                     
          #'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
          'reportName':'CAMPAIGN_PERFORMANCE_REPORT',
          'dateRangeType': 'LAST_7_DAYS',
          #'dateRangeType': 'LAST_30_DAYS',
          'reportType': 'CAMPAIGN_PERFORMANCE_REPORT',
          'downloadFormat': 'CSV',
          'selector': {
              'fields': ['ExternalCustomerId', 'Date', 'AccountDescriptiveName', 'AccountCurrencyCode', 'AccountId','AccountTimeZoneId', 
                    'CampaignId', 'CampaignName', 'CampaignStatus', 'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition',
                    'Conversions','CostPerConversion', 'ConversionRate', 'TotalConvValue', 'ViewThroughConversions','ValuePerConversion']
          },
          # Enable to get rows with zero impressions.
          'includeZeroImpressions': 'false'
      }



    for sCustId in lsCustIds:
        
        print "Downloading custid", sCustId
        logging.info("Downloading custid %s" % sCustId)
        client.SetClientCustomerId(sCustId)
        dlr = client.GetReportDownloader('https://adwords.google.com', 'v201209')
        file_path = dlr.DownloadReport(dlrreport, file_path='/home/ubuntu/dlreports/googCampPerf_' + sCustId + '_Latest.csv')


def dlKeywordPerf(lsCustIds):
    client = getClient()
    #dlr = client.GetReportDownloader('https://adwords.google.com', 'v201209')
    dlrreport = {                     
          #'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
          'reportName':'KEYWORDS_PERFORMANCE_REPORT',
          'dateRangeType': 'LAST_7_DAYS',
          #'dateRangeType': 'LAST_30_DAYS',
          'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
          'downloadFormat': 'CSV',
          'selector': {
              'fields': ['ExternalCustomerId', 'Date', 'AccountDescriptiveName', 'AccountCurrencyCode', 'AccountTimeZoneId', 
                    'CampaignId', 'CampaignName', 'CampaignStatus', 'AdGroupId', 'AdGroupName', 'AdGroupStatus', 'Id', 
                    'KeywordText', 'KeywordMatchType', 'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition','Conversions',
                    'CostPerConversion', 'ConversionRate', 'TotalConvValue', 'ViewThroughConversions','ValuePerConversion']
          },
          # Enable to get rows with zero impressions.
          'includeZeroImpressions': 'false'
      }



    for sCustId in lsCustIds:
        ### just for initial... these are big and time consuming
        if not os.path.exists('/mnt/dlreports/googKeywPerf_' + sCustId + '_Latest.csv'):
            print "Downloading custid", sCustId
            logging.info("Downloading custid %s" % sCustId)
            client.SetClientCustomerId(sCustId)
            dlr = client.GetReportDownloader('https://adwords.google.com', 'v201209')
            #TODO: add try catch for AdWordsReportError: HTTP code: 500, type: 'ReportDownloadError.ERROR_GETTING_RESPONSE_FROM_BACKEND'
            #   and do a retry loop
            file_path = dlr.DownloadReport(dlrreport, file_path='/mnt/dlreports/googKeywPerf_' + sCustId + '_Latest.csv')

def dlGeoPerf(lsCustIds):
    client = getClient()
    #dlr = client.GetReportDownloader('https://adwords.google.com', 'v201209')
    dlrreport = {                     
          #'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
          'reportName':'GEO_PERFORMANCE_REPORT',
          'dateRangeType': 'LAST_7_DAYS',
          #'dateRangeType': 'LAST_14_DAYS',
          #'dateRangeType':'CUSTOM_DATE',
          'reportType': 'GEO_PERFORMANCE_REPORT',
          'downloadFormat': 'CSV',
          'selector': {
              'fields': ['ExternalCustomerId', 'Date', 'AccountDescriptiveName', 'AccountCurrencyCode', 'AccountTimeZoneId', 
                    'CampaignId', 'CampaignName', 'CampaignStatus', 'AdGroupId', 'AdGroupName', 'AdGroupStatus', 'LocationType', 
                    'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId', 'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition','Conversions',
                    'CostPerConversion', 'ConversionRate', 'TotalConvValue', 'ViewThroughConversions','ValuePerConversion'],
                #'dateRange':{'min':'20130101', 'max':'20130121'}
          },
          # Enable to get rows with zero impressions.
          'includeZeroImpressions': 'false'
      }



    for sCustId in lsCustIds:
        if not os.path.exists('/home/ubuntu/dlreports/googGeoPerf_' + sCustId + '_Latest.csv'):
            print "Downloading custid", sCustId
            logging.info("Downloading custid %s" % sCustId)
            client.SetClientCustomerId(sCustId)
            dlr = client.GetReportDownloader('https://adwords.google.com', 'v201209')
            try:
                file_path = dlr.DownloadReport(dlrreport, file_path='/home/ubuntu/dlreports/googGeoPerf_' + sCustId + '_Latest.csv')
            except AdWordsReportError, e:
                #ALSO HAS e.trigger and e.field_path
                if e.http_code == '400' and e.type == 'SizeLimitError.RESPONSE_SIZE_LIMIT_EXCEEDED':
                    ## break it up
                    pass
                raise

                



from decimal import Decimal

#@transaction.commit_on_success
@transaction.commit_manually
def loadCSV(sCustId, sType):
    """
    todo: transactions?
    """
    if sType== "account":
        existingDates = set([o.Date for o in models.GoogleAccountPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId))])

        file_path = '/home/ubuntu/dlreports/googAcctPerf_' + sCustId + '_Latest.csv'
        try:
            p = os.stat(file_path)
        except:
            transaction.rollback()
            return

        with open(file_path, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)
            for i, row in enumerate(csvreader):

                #print ', '.join(row)
                
                if row[0].strip() != "Total" and i not in [0,1]:
                    #print parser.parse(row[1]).date(), existingDates, sCustId
                    if parser.parse(row[1]).date() not in existingDates:
                        print parser.parse(row[1]).date(), existingDates, sCustId
                        #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                        o = models.GoogleAccountPerformanceReport()
                        o.AccountDescriptiveName = row[0]
                        o.Date = parser.parse(row[1]).date()  #models.DateField('Date')
                        o.AccountCurrencyCode = row[2]
                        o.AccountId = int(row[3])
                        o.AccountTimeZoneId = row[4]
                        o.Impressions = int(row[5])
                        o.Clicks = int(row[6])
                        o.Ctr = float(row[7].replace("%", ""))
                        o.AverageCpc = Decimal(row[8])
                        o.Cost = Decimal(row[9].replace(",",""))
                        o.AveragePosition = float(row[10])
                        o.ExternalCustomerId = int(row[11])
                        o.save()

        transaction.commit()

    elif sType== "campaign":
        existingDates = set(models.GoogleCampaignPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId)).values_list('Date', flat=True))
        file_path = '/home/ubuntu/dlreports/googCampPerf_' + sCustId + '_Latest.csv'
        try:
            p = os.stat(file_path)
        except:
            transaction.rollback()
            return

        with open(file_path, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)
            for i, row in enumerate(csvreader):

                #print ', '.join(row)
                
                if row[0].strip() != "Total" and i not in [0,1]:
                    #print parser.parse(row[1]).date(), existingDates, sCustId
                    if parser.parse(row[1]).date() not in existingDates:
                        print parser.parse(row[1]).date(), existingDates, sCustId
                        #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                        o = models.GoogleCampaignPerformanceReport()
                        o.ExternalCustomerId = int(row[0])
                        o.Date = parser.parse(row[1]).date()  #models.DateField('Date')
                        o.AccountDescriptiveName = row[2]
                        o.AccountCurrencyCode = row[3]
                        o.AccountId = int(row[4])
                        o.AccountTimeZoneId = row[5]
                        o.CampaignId = int(row[6])
                        o.CampaignName = row[7]
                        o.CampaignStatus = row[8]
                        o.Impressions = int(row[9])
                        o.Clicks = int(row[10])
                        o.Ctr = float(row[11].replace("%", ""))
                        o.AverageCpc = Decimal(row[12])
                        o.Cost = Decimal(row[13].replace(",",""))
                        o.AveragePosition = float(row[14])
                        o.Conversions = int(row[15])
                        o.CostPerConversion = Decimal(row[16])
                        o.ConversionRate = float(row[17].replace("%", ""))
                        o.TotalConvValue = float(row[18].replace(",",""))
                        o.ViewThroughConversions = int(row[19])
                        o.ValuePerConversion = float(row[20].replace(",",""))
                        o.save()

        transaction.commit()
            

    elif sType== "keyword":
        existingDates = set(models.GoogleKeywordPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId)).values_list('Date', flat=True))

        file_path = '/home/ubuntu/dlreports/googKeywPerf_' + sCustId + '_Latest.csv'
        try:
            p = os.stat(file_path)
        except:
            transaction.rollback()
            return

        with open(file_path, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)


            for i, row in enumerate(csvreader):
                if i % 100 == 0: print i


                if i % 1000 == 0 and i != 0:
                    transaction.commit()

                #print ', '.join(row)
                
                if row[0].strip() != "Total" and i not in [0,1]:
                    #print parser.parse(row[1]).date(), existingDates, sCustId
                    if parser.parse(row[1]).date() not in existingDates:
                        #print parser.parse(row[1]).date(), existingDates, sCustId
                        #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
                        o = models.GoogleKeywordPerformanceReport()
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
                        o.KeywordText = row[12]
                        o.KeywordMatchType = row[13]

                        o.Impressions = int(row[14])
                        o.Clicks = int(row[15])
                        o.Ctr = float(row[16].replace("%", ""))
                        o.AverageCpc = Decimal(row[17])
                        o.Cost = Decimal(row[18].replace(",",""))
                        o.AveragePosition = float(row[19])
                        o.Conversions = int(row[20])
                        o.CostPerConversion = Decimal(row[21])
                        o.ConversionRate = float(row[22].replace("%",""))
                        o.TotalConvValue = float(row[23].replace(",",""))
                        o.ViewThroughConversions = int(row[24])
                        o.ValuePerConversion = float(row[25].replace(",",""))
                        o.save()

            transaction.commit()

    elif sType== "geo":
        #existingDates = set([o.Date for o in models.GoogleGeoPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId))])
        existingDates = set(models.GoogleGeoPerformanceReport.objects.filter(ExternalCustomerId__exact=int(sCustId)).values_list('Date', flat=True))

        file_path = '/home/ubuntu/dlreports/googGeoPerf_' + sCustId + '_Latest.csv'
        try:
            p = os.stat(file_path)
        except:
            transaction.rollback()
            return

        with open(file_path, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)

            for i, row in enumerate(csvreader):
                if i % 100 == 0: print i


                if i % 1000 == 0 and i != 0:
                    transaction.commit()


            

                print ', '.join(row)
                
                if row[0].strip() != "Total" and i not in [0,1]:
                    #print parser.parse(row[1]).date(), existingDates, sCustId
                    if parser.parse(row[1]).date() not in existingDates:
                        print parser.parse(row[1]).date(), sCustId
                    #    'ExternalCustomerId', 'Date', 'AccountDescriptiveName', 'AccountCurrencyCode', 'AccountTimeZoneId', 
                    # 'CampaignId', 'CampaignName', 'CampaignStatus', 'AdGroupId', 'AdGroupName', 'AdGroupStatus', 'LocationType', 
                    # 'CountryCriteriaId', 'RegionCriteriaId', 'MetroCriteriaId', 'CityCriteriaId', 'Impressions','Clicks','Ctr','AverageCpc','Cost','AveragePosition','Conversions',
                    # 'CostPerConversion', 'ConversionRate', 'TotalConvValue', 'ViewThroughConversions','ValuePerConversion'],
                        #Account, Day, Currency, Account ID, Time zone, Impressions, Clicks, CTR, Avg. CPC, Cost, Avg. position
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
                        o.AverageCpc = Decimal(row[19])
                        o.Cost = Decimal(row[20].replace(",",""))
                        o.AveragePosition = float(row[21])
                        o.Conversions = int(row[22])
                        o.CostPerConversion = Decimal(row[23])
                        o.ConversionRate = float(row[24].replace("%",""))
                        o.TotalConvValue = float(row[25].replace(",",""))
                        o.ViewThroughConversions = int(row[26])
                        o.ValuePerConversion = float(row[27].replace(",",""))
                        o.save()

        transaction.commit()

def getEndNodeCustomerIds():
    a,b,c = getAccounts()
    sAllIds = set(b.keys())
    sMgrIds = set(c.keys())
    sEndNodeIds = sAllIds.difference(sMgrIds)
    lsCustIds = list(sEndNodeIds) #[:10]

    return lsCustIds


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




