# -*- coding: utf-8 -*-
import eventlet
eventlet.monkey_patch()
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
from django.db import connection
from django.core.mail import send_mail


TODAY = datetime.date.today()


#### 1) update account info and names
logging.warning("1) update account info and names")

reportr.syncAccountCache()

sSQLCleanCustsForAccess = """
BEGIN;
DROP TABLE IF EXISTS updatr_customers;


CREATE TABLE updatr_customers
(
  "customerId" bigint NOT NULL,
  name character varying(200),
  CONSTRAINT updatr_customers_pkey PRIMARY KEY ("customerId")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE updatr_customers
  OWNER TO lars;
GRANT ALL ON TABLE updatr_customers TO lars;
GRANT SELECT ON TABLE updatr_customers TO reader;

  COMMIT;
"""

sSQLAddCustsForAccess = """
INSERT INTO updatr_customers ("customerId", name)
VALUES (%(customerId)s, '%(name)s');
"""

cursor = connection.cursor()
cursor.execute(sSQLCleanCustsForAccess)
cursor.execute("BEGIN;")
for dCust in models.mongodb.reports.find():
  for k in ['name']:
    if dCust[k] == None:
      dCust[k] = ''
    dCust[k] = dCust[k].replace("%", "%%").replace(r"'", r"''")
  cursor.execute(sSQLAddCustsForAccess % dCust, {})
cursor.execute("COMMIT;")

logging.warning("1) DONE update account info and names")

### Note: we don't worry about subIds right now

##### Add Missing VS and Goog Account Ids to DB and assign to Unassigned
logging.warning("2) Add Missing VS and Goog Account Ids to DB and assign to Unassigned")

reportr.syncMissingAccountsDB()
logging.warning("2) DONE Add Missing VS and Goog Account Ids to DB and assign to Unassigned")

lsCustIds = []
for oMaster in models.MasterAccount.objects.all():
  if oMaster.GoogleMCCId:
    lsCustIds += reportr.getEndNodeCustomerIds(masterId=str(oMaster.GoogleMCCId))

lsCustIds = sorted(lsCustIds)

dates = []
for i in xrange(14): #14

  ## starts with yesterday since today is not finished
  dates.append((TODAY + relativedelta.relativedelta(days=-i-1)).strftime("%Y%m%d"))

dates = sorted(dates)
print dates

#  # reportr.dlAllReports(lsCustIds, dates)
#  # #### DOWNLOAD ##################
#  # iTries = 0
#  # while iTries < 10:
#  #   try:
#  #     reportr.dlAllReports(lsCustIds, dates, force=True)
#  #     break
#  #   except:
#  #     iTries += 1
#  #     eventlet.sleep(iTries * 2)


iNewCallRecords = 0
iNewEmailRecords = 0

##### LOAD DB ##################
logging.warning("3) AG Email logs")

iNewEmailRecords = reportr.loadAGEmailLog(dates)
logging.warning("4) VS Call logs")

iNewCallRecords = reportr.loadVoiceStarCSV(dates, forceupdate=True)

#logging.warning("5) Goog logs")
#reportr.loadCSVByDates(lsCustIds, dates, force=True)


logging.warning("6) Load pivot")
##### UPDATE ANALYTICS
reportr.loadDataTables(days_back=365, update=True, reset=True)


sEmailMsg = """
The LarsReports update script has fully completed.

There were:
%i new email records added
%i new call records added


""" % (iNewEmailRecords, iNewCallRecords)

send_mail('LarsReports Quick Processing Completed', sEmailMsg, 'reports@larsmarketing.com',
    ['larsmarketing@arborheights.net','ryan@larsmarketing.com', 'sarah@larsmarketing.com'], fail_silently=False)


