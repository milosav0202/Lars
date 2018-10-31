

for g in Group.objects.order_by('id'):
    print g.id, g.Name
    bIsGroupMember = True
    if len(g.account_set.filter(ServiceType__exact='2')) > 1:
        #is a true group
        #create a group aao
        gaao = AdAccountOwner()
        gaao.MasterAccount = g.MasterAccount
        gaao.Name = g.Name + " Group"
        gaao.Geo_MetroArea = g.Geo_MetroArea
        gaao.BudgetCurrency = g.BudgetCurrency
        gaao.Budget = g.Budget
        gaao.save()

        for ac in g.account_set.filter(ServiceType__exact='2'):
            aao = AdAccountOwner()
            aao.MasterAccount = g.MasterAccount
            aao.Name = ac.Name
            aao.Geo_MetroArea = g.Geo_MetroArea
            aao.BudgetCurrency = g.BudgetCurrency
            aao.Budget = g.Budget
            #save parent and internal id
            aao.parent = gaao
            if not aao.InternalId: #and not member of a true group:
                aao.InternalId = ac.InternalId

            aao.save()


            ada = AdAccount()

            ada.Active = ac.Active
            ada.ServiceType = ac.ServiceType
            ada.ServiceAccountId = ac.ServiceAccountId
            ada.AdAccountOwner = aao
            ada.save()

        for ac in g.account_set.filter(ServiceType__exact='1'):
            ada = AdAccount()
            ada.Active = ac.Active
            ada.ServiceType = ac.ServiceType
            ada.ServiceAccountId = ac.ServiceAccountId
            ada.AdAccountOwner = gaao
            ada.save()


    else:


        aao = AdAccountOwner()
        aao.MasterAccount = g.MasterAccount
        aao.Name = g.Name
        aao.Geo_MetroArea = g.Geo_MetroArea
        aao.BudgetCurrency = g.BudgetCurrency
        aao.Budget = g.Budget
        #save parent and internal id - parent blank
        aao.save()

        for ac in g.account_set.all():
            ada = AdAccount()
            ada.Active = ac.Active
            ada.ServiceType = ac.ServiceType
            ada.ServiceAccountId = ac.ServiceAccountId
            ada.AdAccountOwner = aao

            if not aao.InternalId: #and not member of a true group:
                aao.InternalId = ac.InternalId
                aao.save()

            ada.save()


