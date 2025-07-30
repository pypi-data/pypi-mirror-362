from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_domain_management.models import *
from adestis_netbox_domain_management.filtersets import *
import django_tables2 as tables
from tenancy.models import *


class DomainTable(NetBoxTable):
    status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )
    
    tenant = tables.Column(
        linkify = True
    )
    
    tenant_group = tables.Column(
        linkify = True
    )
    
    ownerc = tables.Column(
        linkify = True
    )
    
    adminc = tables.Column(
        linkify = True
    )
    
    techc = tables.Column(
        linkify = True
    )
    
    zonec = tables.Column(
        linkify = True
    )
    
    domain = tables.Column(
        linkify = True
    )


    class Meta(NetBoxTable.Meta):
        model = Domain
        fields = ['name', 'tenant', 'created_at', 'reneval_date', 'cancellation_date', 'status', 'comments', 'actions', 'tags', 'created', 'last_updated', 'tenant_group', 'ownerc', 'adminc', 'techc', 'zonec', 'nameserver_1', 'nameserver_2', 'nameserver_3', 'nameserver_4', 'term', 'domain']
        default_columns = ['name', 'tenant', 'created_at', 'reneval_date', 'cancellation_date', 'status',]
