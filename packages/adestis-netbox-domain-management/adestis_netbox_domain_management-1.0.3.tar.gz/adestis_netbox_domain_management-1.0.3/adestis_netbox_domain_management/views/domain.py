from netbox.views import generic
from adestis_netbox_domain_management.forms import *
from adestis_netbox_domain_management.models import *
from adestis_netbox_domain_management.filtersets import *
from adestis_netbox_domain_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from tenancy.models import Tenant, TenantGroup
from tenancy.tables import TenantTable, TenantGroupTable
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view
from django.shortcuts import get_object_or_404, redirect, render

__all__ = (
    'DomainView',
    'DomainListView',
    'DomainEditView',
    'DomainDeleteView',
    'DomainBulkDeleteView',
    'DomainBulkEditView',
    'DomainBulkImportView',
    'TenantAffectedDomainView',
)

class DomainView(generic.ObjectView):
    queryset = Domain.objects.all()


class DomainListView(generic.ObjectListView):
    queryset = Domain.objects.all()
    table = DomainTable
    filterset = DomainFilterSet
    filterset_form = DomainFilterForm

class DomainEditView(generic.ObjectEditView):
    queryset = Domain.objects.all()
    form = DomainForm


class DomainDeleteView(generic.ObjectDeleteView):
    queryset = Domain.objects.all()
 

class DomainBulkDeleteView(generic.BulkDeleteView):
    queryset = Domain.objects.all()
    table = DomainTable
    
    
class DomainBulkEditView(generic.BulkEditView):
    queryset = Domain.objects.all()
    filterset = DomainFilterSet
    table = DomainTable
    form =  DomainBulkEditForm
    

class DomainBulkImportView(generic.BulkImportView):
    queryset = Domain.objects.all()
    model_form = DomainCSVForm
    table = DomainTable

@register_model_view(Tenant, name='domains')
class TenantAffectedDomainView(generic.ObjectChildrenView):
    queryset = Tenant.objects.all()
    child_model= Domain
    table = DomainTable
    template_name = "adestis_netbox_domain_management/domain_tenant.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_tenant': {'change'},
    }

    tab = ViewTab(
        label=_('Domains'),
        badge=lambda obj: obj.domain.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return Domain.objects.restrict(request.user, 'view').filter(tenant=parent)
    