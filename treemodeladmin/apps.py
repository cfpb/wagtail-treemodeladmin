from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WagtailTreeModelAdminAppConfig(AppConfig):
    name = 'treemodeladmin'
    label = 'wagtailtreemodeladmin'
    verbose_name = _("Wagtail TreeModelAdmin")
