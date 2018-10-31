from django.contrib import admin
from main import models 
from django import forms
from django.forms.models import BaseInlineFormSet
from django.contrib.admin import SimpleListFilter
import logging



# class ClientAccountInline(admin.TabularInline):
#     model = models.ClientAccount
#     list_display = ('__unicode__','Account.ServiceType','Account.Active',)
#     list_filter = ('Account.Active', 'Account.ServiceType',)
#     #ordering = ('Account.Name',)



class AccountGroupStateListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Group Status'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'grp_state'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('1', 'Has Subaccounts'),
            ('-1', 'Has Parent'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == '-1':
            return queryset.exclude(subaccounts__isnull=False)

        if self.value() == '1':
            return queryset.filter(subaccounts__isnull=False).distinct()

class AccountUnknownListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Group Assignment'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'is_unknown'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('-1', 'Is Unknown'),
            ('1', 'Is Known'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == '-1':
            return queryset.filter(Group__id__exact=297)

        if self.value() == '1':
            return queryset.exclude(Group__id__exact=297)

class AdAccountUnknownListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Ownership'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'is_unknown'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('-1', 'Is Unknown'),
            ('1', 'Is Known'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == '-1':
            #return queryset.filter(owner__AdAccountOwner__id__exact=208)
            return queryset.filter(owner__isnull=True)


        if self.value() == '1':
            #return queryset.exclude(owner__AdAccountOwner__id__exact=208)
            return queryset.exclude(owner__isnull=True)


# class AccountInline(admin.TabularInline):
#     model = models.Account
#     list_display = ('__unicode__','ServiceType','Active',)
#     list_filter = ('Active', 'ServiceType')
#     extra = 0
#     #ordering = ('Name',)

# class AccountAdminForm(forms.ModelForm):
#     class Meta:
#         model = models.Account

#     def clean_permalink(self): return permalink_cleaner(self)
        
# class AccountAdmin(admin.ModelAdmin):
#     form = AccountAdminForm
#     list_display = ('__unicode__','Group', 'InternalId', 'ServiceType','Active',)
#     list_filter = ('Active', 'ServiceType',AccountUnknownListFilter)
    
#     ordering = ('Group','Name',)
#     search_fields = ['Name']
#     ###takes forever to load
#     #list_editable = ('Group',)
#     #inlines = (ParticipationInline,)
#     #prepopulated_fields = {"permalink": ("name",)}



class AdAccountInlineFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(AdAccountInlineFormset, self).add_fields(form, index)
        avail_accts = models.AdAccount.objects.filter(owner__isnull=True)
        logging.warning(form.instance)
        if form.instance:
            try:        
                owner = form.instance.AdAccountOwner    
            except models.AdAccountOwner.DoesNotExist:
                pass   
            else:
                avail_accts |= models.AdAccount.objects.filter(owner__AdAccountOwner__exact=owner)
        logging.warning(form.fields.keys())
        form.fields['AdAccount'].queryset = avail_accts.order_by('ServiceType', 'ServiceAccountId')

        # landmarks = Landmark.objects.none()
        # if form.instance:
        #     try:        
        #         area = form.instance.area    
        #     except Area.DoesNotExist:
        #         pass   
        #     else:  
        #         landmarks = Landmark.objects.filter(point__within=area.area)
        # form.fields['base_camp'].queryset = landmarks

        
from django.db.models import Q
class AdAccountInline(admin.TabularInline):
    model = models.AdAccountOwnership
    formset = AdAccountInlineFormset
    verbose_name = "Linked Ad Account"
    verbose_name_plural = "Linked Ad Accounts"
    list_display = ('AdAccount.ServiceType','AdAccount.ServiceAccountId','AdAccount.Active',)
    #list_filter = ('Active', 'ServiceType')
    #fields = ('ServiceType','ServiceAccountId','Active',)
    extra = 2
    #ordering = ('Name',)

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     logging.warning(db_field.name)
    #     if db_field.name == "AdAccount":
    #         kwargs["queryset"] = models.AdAccount.objects.filter(Q(owner__isnull=True)|)
    #     #elif db_field.name == "league":
    #     #    kwargs["queryset"] = Org.objects.all().order_by("label")
    #     return super(AdAccountInline, self).formfield_for_foreignkey(db_field, request, **kwargs)



# class AdAccountOwnerForm(forms.ModelForm):

#     class Meta:
#         model = models.AdAccountOwner

#     def __init__(self, *args, **kwargs):
#         super(AdAccountOwnerForm, self).__init__(*args, **kwargs)
#         if self.instance.id:
#             if self.instance.parent:
#                 subaccounts = models.AdAccountOwner.objects.all()
#                 #counties = County.objects.filter(us_state=self.instance.state)
#                 logging.warning(self.fields.keys())
#                 subaccount_field = self.fields['parent'].widget
#                 subaccount_choices = []
#                 if subaccounts is None:
#                     subaccount_choices.append(('', '---------'))

#                 for subaccount in subaccounts:
#                     subaccount_choices.append((subaccount.id, subaccount.Name))
#                 subaccount_field.choices = subaccount_choices


class AdAccountParentInline(admin.TabularInline):
    model = models.AdAccountGrouping
    extra = 2
    fk_name = 'subaccount'
    #verbose_name = "Group Member"
    #verbose_name_plural = "Subaccounts (Group)"


class AdAccountOwnerInline(admin.TabularInline):
    model = models.AdAccountGrouping
    extra = 2
    fk_name = 'parentaccount'
    verbose_name = "Group Member"
    verbose_name_plural = "Subaccounts (Group Members if group - Do not have parents listed here)"

 



    #form = AdAccountOwnerForm

    #list_display = ('__unicode__')
    #readonly_fields = ('Name','InternalId')
    #fields = ['Name','InternalId']
    #list_filter = ('Active', 'ServiceType')
    #ordering = ('Name',)
    # def formfield_for_choice_field(self, db_field, request=None, **kwargs):
    #     if db_field.name == 'parent':
    #         kwargs['choices'] = (('', '---------'), ('1', 'Choice1'), ('2', 'Choice2'))
    #     return db_field.formfield(**kwargs)

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(AdAccountOwnerInline, self).get_form(request, obj, **kwargs)
    #     form.base_fields['parent'].queryset = obj.photos.all()
    #     return form

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "parent":
    #         kwargs["queryset"] = models.AdAccountOwner.objects.all()
    #     return super(AdAccountOwnerInline, self).formfield_for_foreignkey(db_field, request, **kwargs)




class AdAccountAdminForm(forms.ModelForm):
    class Meta:
        model = models.AdAccount

    def clean_permalink(self): return permalink_cleaner(self)
        
class AdAccountAdmin(admin.ModelAdmin):
    form = AdAccountAdminForm
    list_display = ('__unicode__', 'ServiceType','ServiceAccountId', 'Active',)
    list_filter = ('Active', 'ServiceType',AdAccountUnknownListFilter)
    #ordering = ('owner__AdAccountOwner__Name','ServiceType','ServiceAccountId',)
    search_fields = ['ServiceAccountId']
    list_editable = ('Active',)
    ###takes forever to load
    #list_editable = ('Group',)
    #inlines = (ParticipationInline,)
    #prepopulated_fields = {"permalink": ("name",)}

# class GroupAdminForm(forms.ModelForm):
#     class Meta:
#         model = models.Group

#     def clean_permalink(self): return permalink_cleaner(self)
        
# class GroupAdmin(admin.ModelAdmin):
#     form = GroupAdminForm
#     list_display = ('__unicode__','Geo_MetroArea',)
#     inlines = (AccountInline,) 
#     list_editable = ('Geo_MetroArea',)






# class AdAccountOwnerAdminForm(forms.ModelForm):
#     class Meta:
#         model = models.AdAccountOwner

#     def clean_permalink(self): return permalink_cleaner(self)
        
class AdAccountOwnerAdmin(admin.ModelAdmin):
    #form = AdAccountOwnerAdminForm
    list_display = ('__unicode__','InternalId', 'Active') #'Geo_MetroArea',
    inlines = (AdAccountInline,AdAccountOwnerInline,) #AdAccountParentInline)
    list_filter = [AccountGroupStateListFilter]
    ordering = ('MasterAccount__Name', 'Name',)
    list_editable = ('Active',)
    




#admin.site.register(models.LarsClient, LarsClientAdmin)
#admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.MasterAccount)
#admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.AdAccount, AdAccountAdmin)
admin.site.register(models.AdAccountOwner, AdAccountOwnerAdmin)
#admin.site.register(models.GoogleAccountPerformanceReport)
#admin.site.register(models.GoogleCampaignPerformanceReport)
#admin.site.register(models.GoogleKeywordPerformanceReport)
#admin.site.register(models.GoogleGeoPerformanceReport)