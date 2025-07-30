from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'adestis_netbox_domain_management'

router = NetBoxRouter()
router.register('domains', views.DomainViewSet)

urlpatterns = router.urls
