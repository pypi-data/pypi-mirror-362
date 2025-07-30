from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *

__all__ = (
    'DomainStatusChoices',
    'Domain',
)

class DomainStatusChoices(ChoiceSet):
    key = 'Domains.status'

    STATUS_ACTIVE = 'active'
    STATUS_DRAFT = 'draft'
    STATUS_CANCEL_BEFORE_RENEWAL = 'cancel before renewal'
    STATUS_CANCELLED = 'cancelled'
    STATUS_TRANSFERRED_TO_OTHER_PROVIDERS = 'transferred to other provider'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_DRAFT, 'Draft', 'cyan'),
        (STATUS_CANCEL_BEFORE_RENEWAL, 'Cancel before Renewal', 'yellow'),
        (STATUS_CANCELLED, 'Cancelled', 'red'),
        (STATUS_TRANSFERRED_TO_OTHER_PROVIDERS, 'Transferred to Other Provider', 'gray'),
    ]


class Domain(NetBoxModel):

    status = django_models.CharField(
        max_length=50,
        choices=DomainStatusChoices,
        verbose_name='Status',
        help_text='Status'
    )

    comments = django_models.TextField(
        blank=True
    )
    
    name = django_models.CharField(
        max_length=2000
    )
    
    tenant = django_models.ForeignKey(
         to = 'tenancy.Tenant',
         on_delete = django_models.PROTECT,
         related_name = 'domain',
         null = True,
         verbose_name='Tenant',
         blank = True
     )
    
    tenant_group = django_models.ForeignKey(
        to= 'tenancy.TenantGroup',
        on_delete= django_models.PROTECT,
        related_name='domain_tenant_group',
        null = True,
        verbose_name= 'Tenant Group',
        blank = True
    )
    
    ownerc = django_models.ForeignKey(
        to='tenancy.Contact',
        on_delete=django_models.PROTECT,
        related_name='domain_ownerc',
        null=True,
        verbose_name='Owner C' 
    )
    
    adminc = django_models.ForeignKey(
        to='tenancy.Contact',
        on_delete=django_models.PROTECT,
        related_name='domain_adminc',
        null=True,
        verbose_name='Admin C' 
    )
    
    techc = django_models.ForeignKey(
        to='tenancy.Contact',
        on_delete=django_models.PROTECT,
        related_name='domain_techc',
        null=True,
        verbose_name='Tech C' 
    )
    
    zonec = django_models.ForeignKey(
        to='tenancy.Contact',
        on_delete=django_models.PROTECT,
        related_name='domain_zonec',
        null=True,
        verbose_name='Zone C' 
    )
    
    nameserver_1 = django_models.CharField(max_length=255, blank=True, null=True)
    nameserver_2 = django_models.CharField(max_length=255, blank=True, null=True)
    nameserver_3 = django_models.CharField(max_length=255, blank=True, null=True)
    nameserver_4 = django_models.CharField(max_length=255, blank=True, null=True)
    
    created_at = django_models.DateField(
        verbose_name='Created At',
        null=True,
        help_text='Created At (Date)'
    )
    
    renewal_date = django_models.DateField(
        verbose_name='Renewal Date',
        null=True,
        help_text='Renewal Date'
    )
    
    cancellation_date = django_models.DateField(
        verbose_name='Cancellation Date',
        null=True,
        help_text='Cancellation Date',
        required = False
    )
    
    term = django_models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = "Domains"
        verbose_name = 'Domain'

    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_domain_management:domain', args=[self.pk])

    def get_status_color(self):
        return DomainStatusChoices.colors.get(self.status)
