from wagtail_modeladmin.options import ModelAdmin

from treemodeladmin.helpers import TreeAdminURLHelper, TreeButtonHelper
from treemodeladmin.views import (
    TreeCreateView,
    TreeDeleteView,
    TreeEditView,
    TreeIndexView,
)


class TreeModelAdmin(ModelAdmin):
    child_field = None
    child_model_admin = None
    child_instance = None
    parent_field = ""
    index_view_class = TreeIndexView
    create_view_class = TreeCreateView
    delete_view_class = TreeDeleteView
    edit_view_class = TreeEditView
    index_view_extra_css = []
    index_template_name = "treemodeladmin/index.html"
    button_helper_class = TreeButtonHelper
    url_helper_class = TreeAdminURLHelper

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        if self.has_child():
            self.child_instance = self.child_model_admin(parent=self)

    def has_child(self):
        return (
            (self.child_field is not None)
            and (self.child_model_admin is not None)
            and hasattr(self.model, self.child_field)
        )

    def has_parent(self):
        return self.parent is not None and isinstance(
            self.parent, TreeModelAdmin
        )

    def get_child_field(self):
        if self.has_child():
            return self.child_field

    def get_child_name(self):
        if self.has_child():
            return self.child_instance.model._meta.verbose_name

    def get_child_name_plural(self):
        if self.has_child():
            return self.child_instance.model._meta.verbose_name_plural

    def get_parent_field(self):
        if self.has_parent():
            return self.parent_field

    def get_index_view_extra_css(self):
        css = [
            "treemodeladmin/css/index.css",
        ]
        css.extend(self.index_view_extra_css)
        return css

    def get_admin_urls_for_registration(self, parent=None):
        urls = super().get_admin_urls_for_registration()

        if self.has_child():
            urls = urls + self.child_instance.get_admin_urls_for_registration()

        return urls
