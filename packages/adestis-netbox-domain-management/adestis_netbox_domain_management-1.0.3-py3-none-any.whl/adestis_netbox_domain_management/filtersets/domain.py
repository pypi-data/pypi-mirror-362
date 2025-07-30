from adestis_netbox_domain_management.models import Domain
from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q
from django.utils.translation import gettext as _
import django_filters
from tenancy.models import *
from django import forms
from utilities.forms.widgets import DatePicker
from extras.filters import TagFilter
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)

__all__ = (
    'DomainFilterSet',
)

class DomainFilterSet(NetBoxModelFilterSet):
    tags = TagFilter()
    
    nameserver_1 = django_filters.CharFilter(
        required=False
    )
    
    nameserver_2 = django_filters.CharFilter(
        required=False
    )
    
    nameserver_3 = django_filters.CharFilter(
        required=False
    )
    
    nameserver_4 = django_filters.CharFilter(
        required=False
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

    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    
    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant (name)'),
    )
    
    tenant_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        label=_('Tenant Group(ID)'),
    )
    
    tenant_group = DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label=_('Tenant Group (name)'),
    )
    
    ownerc_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Contact.objects.all(),
        label=_('Owner C (ID)'),
    )
    
    ownerc = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Owner C (name)'),
    )
    
    adminc_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Contact.objects.all(),
        label=_('Admin C (ID)'),
    )
    
    adminc = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Admin C (name)'),
    )
    
    techc_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Contact.objects.all(),
        label=_('Tech C (ID)'),
    )
    
    techc = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Tech C (Name)'),
    )
    
    zonec_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Contact.objects.all(),
        label=_('Zone C (ID)'),
    )
    
    zonec = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Zone C (name)'),
    )
    
    term = forms.Textarea(
        # required = False,
        # field_name ='term'
    )
    
    class Meta:
        model = Domain
        fields = ['id', 'name', 'created_at', 'reneval_date', 'cancellation_date', 'tags', 'status', 'comments', 'nameserver_1', 'nameserver_2', 'nameserver_3', 'nameserver_4', 'tenant_group', 'tenant', 'ownerc', 'adminc', 'techc', 'zonec', 'ownerc_id', 'adminc_id', 'techc_id', 'zonec_id', 'term']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter( 
            Q(status__icontains=value) |
            Q(system_url__icontains=value) |
            Q(system_status__icontains=value)
        )
