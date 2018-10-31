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
from pytz import timezone
from dateutil import relativedelta, parser
from ernie import reportr
from main import models
import csv


tzPacific = timezone('US/Pacific')

dYesNo = {
    "Yes": True,
    "No": False
}

def importAG():
    rip = csv.reader(open("/home/ubuntu/lars/ernie/AGEmailHistory.csv", 'rU'))

    for i, row in enumerate(rip):
        if i > 1:
            dt = parser.parse(row[17], fuzzy=True).replace(tzinfo=tzPacific)  #should be tzPacific
            print dt
            print row

            ag = models.AGEmailLog()
            ag.Rid = row[0].strip()
            ag.StoreNum = row[1].strip()
            ag.firstname = row[2].strip()
            ag.lastname = row[3].strip()
            ag.company = row[4].strip()
            ag.address = row[5].strip()
            ag.city = row[6].strip()
            ag.state = row[7].strip()
            ag.zipcode = row[8].strip()
            ag.phone = row[9].strip()
            ag.email = row[10].strip()
            ag.response = row[11].strip()
            ag.projectname = row[12].strip()
            ag.projectduedate = row[13].strip()
            ag.projectdetails = row[14].strip()
            ag.offer = row[15].strip()
            ag.submit = row[16].strip()
            ag.ServerTime = dt.date()
            ag.ServerDateTime = dt
            ag.misc1 = row[18].strip()
            ag.misc2 = row[19].strip()
            ag.misc3 = row[20].strip()
            ag.misc4 = row[21].strip()
            ag.misc5 = row[22].strip()
            ag.save()

def importAGAddition():
    rip = csv.reader(open("/home/ubuntu/lars/ernie/AGEmailHistoryAddition.csv", 'rU'))

    for i, row in enumerate(rip):
        print i, row
        if i > 1:
            dt = parser.parse(row[19], fuzzy=True).replace(tzinfo=tzPacific)  #should be tzPacific
            print dt
            print row

            ag = models.AGEmailLog()
            #ag.Rid = row[0].strip()
            ag.StoreNum = row[0].strip()
            #ag.firstname = row[2].strip()
            ag.lastname = row[4].strip()
            ag.company = row[5].strip().decode('utf-8', 'ignore')
            ag.address = row[6].strip()
            #ag.city = row[6].strip()
            #ag.state = row[7].strip()
            #ag.zipcode = row[8].strip()
            ag.phone = row[8].strip()
            ag.email = row[9].strip()
            ag.response = row[10].strip()
            ag.projectname = row[11].strip()
            ag.projectduedate = row[12].strip()
            ag.projectdetails = row[13].strip().decode('utf-8', 'ignore')
            ag.offer = row[14].strip()
            ag.submit = row[15].strip()
            ag.ServerTime = dt.date()
            ag.ServerDateTime = dt
            #ag.misc1 = row[18].strip()
            #ag.misc2 = row[19].strip()
            #ag.misc3 = row[20].strip()
            #ag.misc4 = row[21].strip()
            #ag.misc5 = row[22].strip()
            ag.save()


# importAGAddition()


