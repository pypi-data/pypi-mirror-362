from adestis_netbox_domain_management.models import Domain
from adestis_netbox_domain_management.filtersets import *
from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import DomainSerializer

class DomainViewSet(NetBoxModelViewSet):
    queryset = Domain.objects.prefetch_related(
        'tags'
    )

    serializer_class = DomainSerializer
    filterset_class = DomainFilterSet