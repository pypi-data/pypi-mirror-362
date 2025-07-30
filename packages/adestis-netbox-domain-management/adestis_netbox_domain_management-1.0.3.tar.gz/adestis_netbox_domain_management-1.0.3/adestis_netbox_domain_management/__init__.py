from netbox.plugins import PluginConfig

class AdestisAccountManagementConfig(PluginConfig):
    name = 'adestis_netbox_domain_management'
    verbose_name = 'Domain Management'
    description = 'A NetBox plugin for managing certficates.'
    version = '1.0.3'
    author = 'ADESTIS GmbH'
    author_email = 'pypi@adestis.de'
    base_url = 'domains'
    required_settings = []
    default_settings = {
        'top_level_menu' : True,
    }

config = AdestisAccountManagementConfig
