from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu
from netbox.choices import ButtonColorChoices
from django.conf import settings

_domains = [
    PluginMenuItem(
        link='plugins:adestis_netbox_domain_management:domain_list',
        link_text='Domains',
        permissions=["adestis_netbox_domain_management.domain_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_domain_management:domain_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_domain_management.domain_add"]),
        )
    ),    
]

plugin_settings = settings.PLUGINS_CONFIG.get('adestis_netbox_domain_management', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(  
        label="Domain Management",
        groups=(
            ("Domains", _domains),
        ),
        icon_class="mdi mdi-earth",
    )
else:
    menu_items = _domains