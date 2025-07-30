from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_domain_management.models import *
from adestis_netbox_domain_management.views import *
from django.urls import include
from utilities.urls import get_model_urls

urlpatterns = (
    # Domains
    path('domains/', DomainListView.as_view(),
         name='domain_list'),
    path('domains/add/', DomainEditView.as_view(),
         name='domain_add'),
    path('domains/delete/', DomainBulkDeleteView.as_view(),
         name='domain_bulk_delete'),
    path('domains/edit/', DomainBulkEditView.as_view(),
         name='domain_bulk_edit'),
    path('domains/import/', DomainBulkImportView.as_view(),
         name='domain_import'),
    path('domains/<int:pk>/',
         DomainView.as_view(), name='domain'),
    path('domains/<int:pk>/',
         include(get_model_urls("adestis_netbox_domain_management", "domain"))),
    path('domains/<int:pk>/edit/',
         DomainEditView.as_view(), name='domain_edit'),
    path('domains/<int:pk>/delete/',
         DomainDeleteView.as_view(), name='domain_delete'),
    path('domains/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='domain_changelog', kwargs={
        'model': Domain
    }),
    
    path('domains/tenants/', TenantAffectedDomainView.as_view(),
         name='domaintenant_list'), 

)
