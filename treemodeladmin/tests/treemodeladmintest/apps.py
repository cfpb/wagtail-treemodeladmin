from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TreeModelAdminTestAppConfig(AppConfig):
    name = "treemodeladmin.tests.treemodeladmintest"
    label = "treemodeladmintest"
    verbose_name = _("Test Tree Model Admin")
    default_auto_field = "django.db.models.AutoField"
