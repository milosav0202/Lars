# -*- coding: utf-8 -*-
from djangomako.shortcuts import render_to_response, render_to_string
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.http import HttpResponse
from django.template import RequestContext

from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time, json, datetime, pytz
import dateutil.parser
import models

from ernie import reportr
import zipfile

DISPLAY_TZ = pytz.timezone("US/Pacific")


@login_required
def ajax_generateReportSet(request):
    if request.method == 'POST':
        dtNow = datetime.datetime.now(pytz.utc).astimezone(DISPLAY_TZ)
        #get params - daterange, clientIds

        # daterange = request.POST['daterange']
        # start, end = [x.strip() for x in daterange.split("-", 1)]

        # dtStart = dateutil.parser.parse(start)
        # dtEnd = dateutil.parser.parse(end)

        # lsDates = reportr.getStrDates(dtStart, dtEnd)


        monthSelector = request.POST['monthSelector']
        dtMonth = dateutil.parser.parse(monthSelector)
        

        clientIds = []
        for key in request.POST.keys():
            if key[:6] == "check_":
                clientIds.append(request.POST[key])

        reportlabel = request.POST['reportlabel']



        # ## generate
        # reportr.dumpToXl(clientIds, lsDates, reportName=reportlabel, timestamp=dtNow)
        


        # ##zip file too
        paths = []
        for cid in clientIds:   
        #     sAcctName = models.mongodb.reports.find_one({'customerId':cid})['name']
        #     paths.append('%s_%s_%s.xls' % (dtNow.strftime("%Y%m%d"), reportlabel, sAcctName))
            try:
                aao = models.AdAccountOwner.objects.get(id=cid)
            except:
                continue
            reportr.dumpAGXLv2(cid, dtMonth.month, dtMonth.year,timestamp=dtNow)

            oSubaccounts = [sa.subaccount for sa in aao.subaccounts.filter(subaccount__Active__exact=True)]

            if aao.InternalId:
                sGroupIds = aao.InternalId
            else:
                sGroupIds = ", ".join(sorted([sa.InternalId for sa in oSubaccounts]))
            
            reportName = aao.MasterAccount.Name.replace("/", "-") + "_" + aao.Name.replace("/", "-") + "_" + sGroupIds.replace(", ", "+")
            sAcctName = aao.Name
            #paths.append('%s_%s_%s.xls' % (dtNow.strftime("%Y%m%d"), reportlabel, sAcctName))
            #paths.append('%s_%s_%s.xls' % (dtNow.strftime("%Y%m"), reportlabel, sAcctName))
            paths.append('%s%02d_%s_v%s.xls' % (unicode(dtMonth.year), dtMonth.month, reportName, dtNow.strftime("%Y%m%d"), ))


        sDateMade = dtNow.strftime("%Y%m%dT%H%M%S")

        if len(clientIds) > 1:
            zipName = "%s_%s.zip" % (sDateMade, reportlabel)
        else:
            zipName = "%s_%s.zip" % (sDateMade, reportName)

        zBatch = zipfile.ZipFile(reportr.REPORT_DUMP_PATH + zipName,'w')
        for path in paths:
            print path
            if os.path.exists(reportr.REPORT_DUMP_PATH + path):
                zBatch.write(reportr.REPORT_DUMP_PATH + path, path)
            
        zBatch.close()

        return HttpResponse(json.dumps([[dtNow.strftime("%Y%m%dT%H:%M:%S"), zipName]] + [[dtNow.strftime("%Y%m%dT%H:%M:%S"), path] for path in paths] ))


        

# def sync(request):
#     lsGoog = models.mongodb.reports.find()
#     lsMasters = models.MasterAccount.objects.all()

#     sGids = set([x.ServiceAccountId for x in models.Account.objects.filter(ServiceType__exact=1)])
#     sAllGids = set([x['customerId'] for x in lsGoog])

#     sNew = sAllGids.difference(sGids)
#     sRemoved = sGids.difference(sAllGids)

#     lsNew = models.mongodb.reports.find({'customerId':{'$in':list(sNew)}})

#     return render_to_response('main/sync.mko', {'lsNew':lsNew, 'lsRemoved':[], 'lsMasters':lsMasters}, context_instance=RequestContext(request)) 

@login_required
def index(request):

    # def mongoToTree(key, dClients):

    #     dTree = { 
    #         "data" : dClients[key]['name'], 
    #         #// omit `attr` if not needed; the `attr` object gets passed to the jQuery `attr` function
    #         "attr" : { "id" : dClients[key]['customerId']}, 
    #         #// `state` and `children` are only used for NON-leaf nodes
    #         "state" : "closed", #// or "open", defaults to "closed"
    #         "children" : [ mongoToTree(subid, dClients) for subid in dClients[key]['subIds'] ]
    #     }
        
    #     return dTree



    # path to the directory (relative or absolute)
    dirpath = "/home/ubuntu/lars/static/reportExport"

    # get all entries in the directory w/ stats
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries)

    # leave only regular files, insert creation date
    entries = ((stat[ST_CTIME], path)
               for stat, path in entries if S_ISREG(stat[ST_MODE]))
    #NOTE: on Windows `ST_CTIME` is a creation date 
    #  but on Unix it could be something else
    #NOTE: use `ST_MTIME` to sort by a modification date

    lsReports = []
    for i, (cdate, path) in enumerate(sorted(entries, reverse=True)):

        if os.path.basename(path)[0] != ".":
            lsReports.append((pytz.utc.localize(datetime.datetime.fromtimestamp(cdate)).astimezone(DISPLAY_TZ), os.path.basename(path)))


    ## Add the MasterAccounts to the dClient list
    clients = models.MasterAccount.objects.all()
    dTree = []
    #dClients = dict([(x['customerId'], x) for x in clients])
    dClients = dict([(x.id, x) for x in clients] )

    ## Add the rest of the active account owners
    for aao in models.AdAccountOwner.objects.filter( Active__exact=True):
    #for aao in val.adaccountowner_set.filter(adaccounts__AdAccountOwner__Active__exact=True):
        dClients[aao.id] = aao

    # for dCl in dClients.itervalues():

    #     if dCl['subIds']:
    #         dTree.append(mongoToTree(dCl['customerId'], dClients))
    # jsTreeData = json.dumps(dTree)



    return render_to_response('main/index.mko', {'user':request.user, 'reports':lsReports, 'clients':dClients}, context_instance=RequestContext(request))  #, 'jsTreeData':jsTreeData

#def print_index_view(request):
#    print render_to_string('index.html', {'user':request.user})
