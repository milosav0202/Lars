# -*- coding: utf-8 -*-
import sys, os, logging, collections, time, operator
PROJECT_ROOT = os.path.abspath( 
    os.path.dirname(__file__) + "../.." 
)
sys.path = [PROJECT_ROOT] + sys.path   
from django.core.management import setup_environ
from lars import settings
setup_environ(settings)

from ernie import reportr
from main import models

cl  = reportr.getClient()
#cc = reportr.getEndNodeCustomerIds()
cc = reportr.getAccountsByParent('6061785237')


#grps2 = models.AdAccountOwner.objects.filter(MasterAccount__exact=2, parental__isnull=True, Active__exact=True)  #top level account owners
#for g in grps2:                                                                          
 #  dumpAGXLv2(g.id

def getCampaignIds(client_id):
    cl.SetClientCustomerId(client_id)
    cs =  cl.GetCampaignService(version='v201306')
    tResult = cs.get({"fields":["Id", "Name"]})
    if tResult[0].has_key('entries'):
        return [x['id'] for x in tResult[0]['entries']]
    else:
        return []


def getAdExt():
    dd = {}
    for c in cc:
        print c
        cl.SetClientCustomerId(c)
        #aa = models.AdAccount.objects.get(ServiceAccountId__exact=c)
        # aeo = cl.GetAdExtensionOverrideService()
        # x = aeo.Get({'paging':{}, 'statuses':[], 'campaignIds':[]})
        # print x
        # if x[0].has_key('entries') and len(x[0]['entries']) > 0:
        #     subd = x[0]['entries'][0]
        #     subd['_googleId'] = c
        #     dd[x[0]['entries'][0]['adExtension']['id']] = subd

        aeo = cl.GetCampaignAdExtensionService(version='v201306')
        x = aeo.Get({'paging':{'startIndex':'0', 'numberResults':'400'}, 'fields':['Address']})
        if x[0].has_key('entries') and len(x[0]['entries']) > 0:
            subd = x[0]['entries'][0]
            #subd['_googleId'] = c
            dd[c] = x[0]['entries']
    return dd

#Allentown = '3137836330'
#Albuquerque = '3548252178'

def removeAdExt(client_id):
    cids = getCampaignIds(client_id)
    if cids:

        cl.SetClientCustomerId(client_id)
        aeo = cl.GetCampaignAdExtensionService(version='v201306')
      #   selector = {
      #     'addresses': [
      #         {
      #             'streetAddress': '1600 Amphitheatre Parkway',
      #             'cityName': 'Mountain View',
      #             'provinceCode': 'US-CA',
      #             'provinceName': 'California',
      #             'postalCode': '94043',
      #             'countryCode': 'US'
      #         },
      #         {
      #             'streetAddress': '38 avenue de l\'Opéra',
      #             'cityName': 'Paris',
      #             'postalCode': '75002',
      #             'countryCode': 'FR'
      #         }
      #     ]
      # }


        #cids = ['118537092','118537212']

        selector = {
                'predicates':[
                    {'field': 'CampaignId',
                    'operator': 'IN',
                    'values': cids},
                    {'field':'Status',
                    'operator': 'EQUALS',
                    'values': ['ACTIVE']}


                 ],
                'fields':['Address', 'PhoneNumber'],
                'paging':{'startIndex':'0', 'numberResults':'400'}
            }

        geo_locations = aeo.Get(selector)
        #print geo_locations

        dOperations = collections.defaultdict(dict)
        for cid in cids:
            print ">>>", cid
            if geo_locations[0].has_key('entries'):
                lsOrigWithPhoneNums = [d for d in geo_locations[0]['entries'] if d['adExtension']['AdExtension_Type'] == 'LocationExtension' 
                    and d['adExtension'].has_key('phoneNumber') and d['campaignId'] == cid]

                dUpdated = {}
                for dWithPhoneNum in lsOrigWithPhoneNums:
                    dEdit = dWithPhoneNum.copy()
                    aeid = dEdit['adExtension']['id']
                    print aeid, dEdit

                    del dEdit['adExtension']['id']
                    dEdit['adExtension']['phoneNumber'] = ''
                    #print aeid, dEdit
                    dUpdated[aeid] = dEdit




                for k,v in dUpdated.iteritems():
                    operations = [
                      {
                          'operator': 'REMOVE',
                          'operand': {
                              'xsi_type': 'CampaignAdExtension',
                              'campaignId': v['campaignId'],
                              'adExtension': {
                                  'id':k
                              }
                          }
                      },
                      {
                          'operator': 'ADD',
                          'operand': {
                              'xsi_type': 'CampaignAdExtension',
                              'campaignId': v['campaignId'],
                              'adExtension': v['adExtension'],
                              'approvalStatus':'APPROVED'
                          }
                      }
                    ]
                    dOperations[cid][k] = operations

                    print operations



        for cid,v in dOperations.iteritems():
            for aeid, ops in v.iteritems():
                print aeo.Mutate(ops)[0]
                print
                print


        return dOperations
    #now, remove, then add back

    # Construct operations and add campaign ad extension.
    # operations = [
    #   {
    #       'operator': 'ADD',
    #       'operand': {
    #           'xsi_type': 'CampaignAdExtension',
    #           'campaignId': campaign_id,
    #           'adExtension': {
    #               'xsi_type': 'LocationExtension',
    #               'address': geo_locations[0]['address'],
    #               'geoPoint': geo_locations[0]['geoPoint'],
    #               'encodedLocation': geo_locations[0]['encodedLocation'],
    #               'source': 'ADWORDS_FRONTEND',
    #               # Optional fields.
    #               'companyName': 'ACME Inc.',
    #               'phoneNumber': '(650) 253-0000'
    #           }
    #       }
    #   },
    #   {
    #       'operator': 'ADD',
    #       'operand': {
    #           'xsi_type': 'CampaignAdExtension',
    #           'campaignId': campaign_id,
    #           'adExtension': {
    #               'xsi_type': 'LocationExtension',
    #               'address': geo_locations[1]['address'],
    #               'geoPoint': geo_locations[1]['geoPoint'],
    #               'encodedLocation': geo_locations[1]['encodedLocation'],
    #               'source': 'ADWORDS_FRONTEND'
    #           }
    #       }
    #   }
    # ]

    # operations = [
    #     {
    #       'operator': 'REMOVE',
    #       'operand': {
    #           'xsi_type': 'CampaignAdExtension',
    #           'campaignId': campaign_id,
    #           'adExtension': {
    #               'xsi_type': 'LocationExtension',
    #               'phoneNumber':
    #           }
    #       }
    #   }

    # ]
    # ad_extensions = aeo.Mutate(operations)[0]

    # # Display results.
    # for ad_extension in ad_extensions['value']:
    #     print ('Campaign ad extension with id \'%s\' and status \'%s\' was added.'
    #            % (ad_extension['adExtension']['id'], ad_extension['status']))

import csv

def dumpToCSV(dd):
    dAdExtensionKeys = collections.defaultdict(list)
    lsStatsKeys = None
    lsRows = []
    lsBadKeys = ['encodedLocation', 'geoPoint']

    for k,v in dd.iteritems():
        

        for dExt in v:
            if not dAdExtensionKeys.has_key(dExt['adExtension']['AdExtension_Type']): 
                dAdExtensionKeys[dExt['adExtension']['AdExtension_Type']] = dExt['adExtension'].keys()
                for badk in lsBadKeys:
                    try:
                        dAdExtensionKeys[dExt['adExtension']['AdExtension_Type']].remove(badk)
                    except ValueError:
                        pass
            if not lsStatsKeys:
                lsStatsKeys = dExt['stats'].keys()

    for k,v in dd.iteritems():
        sName = ""
        aa = models.AdAccount.objects.get(ServiceAccountId__exact=k)
        if aa:
            aaos = aa.owner.all()
            if aaos:
                sName = aaos[0].AdAccountOwner.Name
        for dExt in v:

            lsRow = [sName, dExt['campaignId']] 
            for extt in sorted(dAdExtensionKeys.iterkeys()):
                # if extt == 'LocationExtension':
                #     if dExt['adExtension']['AdExtension_Type'] == 'LocationExtension' and dExt['adExtension'].has_key('address'):
                #         print dExt['adExtension']['address']
                #         sAddress = ", ".join([dExt['adExtension']['address'][addrk] for addrk in ['streetAddress', 'cityName', 'provinceName', 'countryCode', 'postalCode'] if dExt['adExtension']['address'].has_key(addrk)])
                #         lsRow.append(sAddress)
                #     else:
                #         lsRow.append("")

                for sk in dAdExtensionKeys[extt]:
                    if sk == "AdExtension_Type":
                        lsRow.append(dExt['adExtension'].get(sk, 'N/A'))
                    elif dExt['adExtension']['AdExtension_Type'] == extt and sk == 'address':
                        if dExt['adExtension'].has_key('address'):
                            sAddress = ", ".join([dExt['adExtension']['address'][addrk] for addrk in ['streetAddress', 'cityName', 'provinceName', 'countryCode', 'postalCode'] if dExt['adExtension']['address'].has_key(addrk)])
                            lsRow.append(sAddress)
                        else:
                            lsRow.append("N/A")

                    elif dExt['adExtension']['AdExtension_Type'] == extt:
                        lsRow.append(dExt['adExtension'].get(sk, 'N/A'))
                    else:
                        lsRow.append("N/A")

                
            lsRow += [dExt['stats'][ssk] for ssk in lsStatsKeys]

            lsRows.append(lsRow)


    lsHeaderRow = ["Name", "campaignId"]
    for extt in sorted(dAdExtensionKeys.iterkeys()):
        #if extt == 'LocationExtension':
            
        lsHeaderRow += dAdExtensionKeys[extt]
    lsHeaderRow += lsStatsKeys

    with open('AGadExtensions.csv', 'wb') as f:
        writer = csv.writer(f)
        
        writer.writerow(lsHeaderRow )
        writer.writerows(lsRows)



#for k,v in dd.iteritems():
#    print v['adExtension']['address']