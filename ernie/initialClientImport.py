#Client_ID,Client_Name,Group_ID,Center_Number,VS_ID,Active,Group,Current_Monthly_Budget,Metro_Area,State_Code,Google_Customer_ID,Adcenter_Account_ID,Active
import sys, os, logging, collections, time, operator
PROJECT_ROOT = os.path.abspath( 
    os.path.dirname(__file__) + "../.." 
)
sys.path = [PROJECT_ROOT] + sys.path   
from django.core.management import setup_environ
from lars import settings
setup_environ(settings)

import datetime, pytz
from dateutil import relativedelta
from ernie import reportr
from main import models
import csv




dYesNo = {
	"Yes": True,
	"No": False
}

def importToDicts():
	rip = csv.reader(open("/home/ubuntu/lars/ernie/ClientGroupExport.csv", 'rU'))

	dAccounts = {}
	dAccountIdByName = {}
	dGroups = {}
	for i, row in enumerate(rip):
		if i > 1:
			#if not dAccounts.has_key(int(row[0])):
			dAccounts[int(row[0])] = {"Name": row[1], "vsid": row[4], 'gid':row[2], 'vsactive': row[5]	}
			dAccountIdByName[row[1]] = int(row[0])
			if not dGroups.has_key(int(row[2])):
				dGroups[int(row[2])] = {"Name": row[6], "Budget": int(row[7]), 'gooid':row[10], 'adcid':row[11], 'groupactive':row[12], "cids":[]}
			
			dGroups[int(row[2])]['cids'].append(int(row[0]))

	#patch a dup
	dGroups[91]['Name'] = 'Sycamore two'
	#return dAccounts, dGroups



	###### Add Groups

	# for oldid, dGrp in dGroups.iteritems():
	# 	grp = models.Group(MasterAccount_id=2, Name=dGrp["Name"], Budget=dGrp["Budget"])
	# 	grp.save()
	# 	dGroups[oldid]['newid'] = grp.id

	for oldid, dGrp in dGroups.iteritems():
		grp = models.Group.objects.get(MasterAccount_id=2, Name=dGrp["Name"])
	 	dGroups[oldid]['newid'] = grp.id



	


	# for oldid, dc in dGroups.iteritems(): 
	# 	if dc['gooid']:
	# 		gacct = models.Account(Name=dc['Name'], 
	# 			Active=dYesNo[dc['groupactive']],
	# 			#Shared=bool(len(da['cids'])> 1),
	# 			ServiceType='1',
	# 			ServiceAccountId=dc['gooid'],
	# 			Group_id=dc['newid'])


	# 		gacct.save()
		
	# 	if dc['adcid'] and dc['adcid'] != '0':
	# 		adcacct = models.Account(Name=dc['Name'], 
	# 				Active=dYesNo[dc['groupactive']],
	# 				ServiceType='3',
	# 				ServiceAccountId=dc['adcid'],
	# 				Group_id=dc['newid'])


	# 		adcacct.save()


	# 	for aid in dc['cids']:
	# 		print aid
	# 		da = dAccounts[aid]
	# 		if da["vsid"]:
	# 			#print cl.Name,dYesNo[dAccounts[dAccountIdByName[cl.Name]]['vsactive']],False,2,dAccounts[dAccountIdByName[cl.Name]]['vsid']
	# 			print da['Name'], dc['Name']
	# 			##!!!!!###!!!!!
	# 			vsacct = models.Account(Name=da['Name'], 
	# 				Active=dYesNo[da['vsactive']],
	# 				ServiceType='2',
	# 				ServiceAccountId=da['vsid'],
	# 				Group_id=dc['newid'])


	# 			vsacct.save()

	return dAccounts, dGroups

	# # for cl in models.LarsClient.objects.all():

	# # 	#cl, bCreated = models.LarsClient.objects.get_or_create(Name=dc['Name'])

	# # 	##Add vs acct
		
		# if dAccounts[dAccountIdByName[cl.Name]]["vsid"]:
		# 	#print cl.Name,dYesNo[dAccounts[dAccountIdByName[cl.Name]]['vsactive']],False,2,dAccounts[dAccountIdByName[cl.Name]]['vsid']

		# 	##!!!!!###!!!!!
		# 	vsacct = models.Account(Name=cl.Name, 
		# 		Active=dYesNo[dAccounts[dAccountIdByName[cl.Name]]['vsactive']],
		# 		Shared=False,
		# 		ServiceType='2',
		# 		ServiceAccountId=dAccounts[dAccountIdByName[cl.Name]]['vsid'])


		# 	vsacct.save()

	# 		###!!!!!###!!!!!
	# # 		cavs = models.ClientAccount(Client=cl, Account=vsacct)
	# # 		cavs.save()




	# for da in dGroups.itervalues():
	# 	# if da['gooid']:
	# 	# 	print da['Name'], dYesNo[da['groupactive']] ,bool(len(da['cids'])> 1),'1',da['gooid']

	# 	###!!!!!
	# 	# 	gacct = models.Account(Name=da['Name'], 
	# 	# 		Active=dYesNo[da['groupactive']],
	# 	# 		Shared=bool(len(da['cids'])> 1),
	# 	# 		ServiceType='1',
	# 	# 		ServiceAccountId=da['gooid'])


	# 	# 	gacct.save()

	# 	# 	for oldid in da['cids']:

	# 			###!!!!!
	# 	# 		cl = models.LarsClient.objects.get(Name=dAccounts[oldid]['Name'])
	# 	# 		print "\t", cl.Name
	# 	# 		cag = models.ClientAccount(Client=cl, Account=gacct)
	# 	# 		cag.save()

	# 	if da['adcid'] and da['adcid'] != '0':
	# 		print da['Name'], dYesNo[da['groupactive']] ,bool(len(da['cids'])> 1),'3',da['adcid']
	# 		adcacct = models.Account(Name=da['Name'], 
	# 			Active=dYesNo[da['groupactive']],
	# 			Shared=bool(len(da['cids'])> 1),
	# 			ServiceType='3',
	# 			ServiceAccountId=da['adcid'])


	# 		adcacct.save()

	# 		for oldid in da['cids']:
	# 			###!!!!!
	# 			cl = models.LarsClient.objects.get(Name=dAccounts[oldid]['Name'])
	# 			print "\t", cl.Name
	# 			###!!!!!
	# 			caadc = models.ClientAccount(Client=cl, Account=adcacct)
	# 			caadc.save()





			# Name = models.CharField('Account Name', max_length=120, unique=True)
   #  Active = models.BooleanField("Is Active?", default=True)
   #  Shared = models.BooleanField("Is Shared?", default=False)
   #  ServiceType = models.CharField("Service Type", max_length=30, choices=((1,'Google AdWords'),(2,'VoiceStar'),(3,'AdCenter')))
   #  ServiceAccountId = models.CharField('Account ID', max_length=80, blank=False)


		##Add goo acct


		##Add Adcenter acct


	##Join em up

	# ac = models.Account()
	# Account(models.Model):
 #    Name = models.CharField('Account Name', max_length=120, unique=True)
 #    Active = models.BooleanField("Is Active?", default=True)
 #    Shared = models.BooleanField("Is Shared?", default=False)
 #    ServiceType = models.CharField("Service Type", max_length=30, choices=((1,'Google AdWords'),(2,'VoiceStar'),(3,'AdCenter')))
 #    ServiceAccountId = models.CharField('Account ID', max_length=80, blank=False)
 #    BudgetCurrency = models.CharField("Budget Currency", max_length=5, default="USD", choices=((k,v["CurrencyName"]) for k,v in D_CURRENCY_CODES.iteritems()) )
 #    Budget = models.DecimalField("Budget", max_digits=10, decimal_places=2, blank=True, null=True)
 #    #BudgetDuration = models.ChoiceField("Budget Duration", choices=['Month', 'Day'], default="Month")
 #    Geo_MetroArea
