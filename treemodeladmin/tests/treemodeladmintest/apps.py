from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TreeModelAdminTestAppConfig(AppConfig):
    name = 'treemodeladmin.tests.treemodeladmintest'
    label = 'test_treemodeladmintest'
    verbose_name = _("Test Tree Model Admin")
