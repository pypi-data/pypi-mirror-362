from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_domain_management.models.domain import Domain, DomainStatusChoices
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from tenancy.models import Tenant, TenantGroup, Contact, ContactGroup
from utilities.forms.widgets import DatePicker
from utilities.forms import ConfirmationForm

__all__ = (
    'DomainForm',
    'DomainFilterForm',
    'DomainBulkEditForm',
    'DomainCSVForm',
    'DomainAssignTenantGroupForm',
    'DomainRemoveTenantGroup',
    'DomainAssignTenantForm',
)

class DomainForm(NetBoxModelForm):
    comments = CommentField()

    tenant_group = DynamicModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        null_option='None',
    )

    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        query_params={
            'group_id': '$tenant_group'
        },
    )
    
    ownerc = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label='Owner C'
        
    )
    
    adminc = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label='Admin C'
    )
    
    techc = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label='Tech C'
    )
    
    zonec = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label='Zone C'
    )
    
    fieldsets = (
        FieldSet('name', 'created_at', 'reneval_date', 'cancellation_date', 'tags', 'status', 'comments', name=_('Domain')),
        FieldSet('nameserver_1', 'nameserver_2', 'nameserver_3', 'nameserver_4', name=_('Nameserver')),
        FieldSet('tenant_group', 'tenant',  name=_('Tenant')),
        FieldSet('ownerc', 'adminc', 'techc', 'zonec', name=_('Contact')),
        FieldSet('term', name=_('Term'))
    )

    class Meta:
        model = Domain
        fields = ['name', 'created_at', 'reneval_date', 'cancellation_date', 'tags', 'status', 'comments', 'nameserver_1', 'nameserver_2', 'nameserver_3', 'nameserver_4', 'tenant_group', 'tenant', 'ownerc', 'adminc', 'techc', 'zonec', 'term']
        help_texts = {
            'status': "Status",
        }
        widgets = {
            'created_at': DatePicker(),
            'reneval_date': DatePicker(),
            'cancellation_date': DatePicker(),
        }


class DomainBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Domain.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
    )
    
    created_at = forms.DateField(
        required=False,
        widget=DatePicker
    )
    
    reneval_date = forms.DateField(
        required=False,
        widget=DatePicker
    )
    
    cancellation_date = forms.DateField(
        required=False,
        widget=DatePicker
    )
    
    comments = forms.CharField(
        max_length=150,
        required=False,
        label=_("Comment")
    )

    status = forms.ChoiceField(
        required=False,
        choices=DomainStatusChoices,
    )
    
    tenant_group = DynamicModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        null_option='None',
    )

    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        query_params={
            'group_id': '$tenant_group'
        },
    )
    
    ownerc = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label='Owner C'
    )
    
    adminc = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label='Admin C'
    )
    
    techc = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label='Tech C'
    )
    
    zonec = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label='Zone C'
    )

    model = Domain

    fieldsets = (
        FieldSet('name', 'created_at', 'reneval_date', 'cancellation_date', 'tags', 'status', 'comments', name=_('Domain')),
        FieldSet('nameserver_1', 'nameserver_2', 'nameserver_3', 'nameserver_4', name=_('Nameserver')),
        FieldSet('tenant_group', 'tenant',  name=_('Tenant')),
        FieldSet('ownerc', 'adminc', 'techc', 'zonec', name=_('Contact')),
        FieldSet('term', name=_('Term'))
    )

    nullable_fields = [
         'add_tags', 'remove_tags'
    ]


class DomainFilterForm(NetBoxModelFilterSetForm):
    
    model = Domain

    fieldsets = (
        FieldSet('name', 'created_at', 'reneval_date', 'cancellation_date', 'tags', 'status', 'comments', name=_('Domain')),
        FieldSet('nameserver_1', 'nameserver_2', 'nameserver_3', 'nameserver_4', name=_('Nameserver')),
        FieldSet('tenant_group_id', 'tenant_id',  name=_('Tenant')),
        FieldSet('ownerc_id', 'adminc_id', 'techc_id', 'zonec_id', name=_('Contact')),
        # FieldSet('term', name=_('Term'))
    )

    index = forms.IntegerField(
        required=False
    )
    
    name = forms.CharField(
        max_length=200,
        required=False
    )
    
    created_at = forms.DateField(
        required=False
    )
    
    reneval_date = forms.DateField(
        required=False
    )
    
    cancellation_date = forms.DateField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=DomainStatusChoices,
        required=False,
        label=_('Status')
    )
    
    nameserver_1 = forms.CharField(
        max_length=200,
        required=False
    )
    
    nameserver_2 = forms.CharField(
        max_length=200,
        required=False
    )
    
    nameserver_3 = forms.CharField(
        max_length=200,
        required=False
    )
    
    nameserver_4 = forms.CharField(
        max_length=200,
        required=False
    )
    
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        query_params={
            'group_id': '$tenant_group_id'
        },
        label=_('Tenant')
    )
    
    tenant_group_id = DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label=_('Tenant Group')
    )
    
    ownerc_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Owner C')
    )
    
    adminc_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Admin C')
    )
    
    techc_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Tech C')
    )
    
    zonec_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Zone C')
    )
    term = forms.TextInput()

    tag = TagFilterField(model)


class DomainCSVForm(NetBoxModelImportForm):

    status = CSVChoiceField(
        choices=DomainStatusChoices,
        help_text=_('Status'),
        required=True,
    )
    
    tenant_group = CSVModelChoiceField(
        label=_('Tenant Group'),
        queryset=TenantGroup.objects.all(),
        required=True,
        to_field_name='name',
        help_text=('Name of assigned tenant group')
    )
    
    tenant = CSVModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned tenant')
    )
    
    ownerc = CSVModelChoiceField(
        label=_('Owner C'),
        queryset=Contact.objects.all(),
        required=True,
        to_field_name='name',
        help_text=('Name of assigned Owner C')
    )
    
    adminc = CSVModelChoiceField(
        label=_('Admin C'),
        queryset=Contact.objects.all(),
        required=True,
        to_field_name='name',
        help_text=('Name of assigned Admin C')
    )
    
    techc = CSVModelChoiceField(
        label=_('Tech C'),
        queryset=Contact.objects.all(),
        required=True,
        to_field_name='name',
        help_text=('Name of assigned Tech C')
    )
    
    zonec = CSVModelChoiceField(
        label=_('Zone C'),
        queryset=Contact.objects.all(),
        required=True,
        to_field_name='name',
        help_text=('Name of assigned Zone C')
    )

    class Meta:
        model = Domain
        fields = ['name', 'created_at', 'reneval_date', 'cancellation_date', 'tags', 'status', 'comments', 'nameserver_1', 'nameserver_2', 'nameserver_3', 'nameserver_4', 'tenant_group', 'tenant', 'ownerc', 'adminc', 'techc', 'zonec', 'term']
        default_return_url = 'plugins:adestis_netbox_domain_management:domain_list'

class DomainAssignTenantGroupForm(forms.Form):
    
    tenant_group = DynamicModelMultipleChoiceField(
        label=_('Tenant Group'),
        queryset=TenantGroup.objects.all()
    )

    class Meta:
        fields = [
            'tenant_group',
        ]

    def __init__(self, domain, *args, **kwargs):

        self.domain = domain

        self.tenant_group = DynamicModelMultipleChoiceField(
            label=_('Tenant Groups'),
            queryset=TenantGroup.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['tenant_group'].choices = [] 
        
class DomainRemoveTenantGroup(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    

    
    
class DomainAssignTenantForm(forms.Form):
    
    tenant = DynamicModelMultipleChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all()
    )

    class Meta:
        fields = [
            'tenant',
        ]

    def __init__(self, domain, *args, **kwargs):

        self.domain = domain

        self.tenant = DynamicModelMultipleChoiceField(
            label=_('Tenant'),
            queryset=Tenant.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['tenant'].choices = [] 
        
class DomainRemoveTenant(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    
