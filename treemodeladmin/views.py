from django.contrib.admin.utils import unquote
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.functional import cached_property

from wagtail.contrib.modeladmin.views import IndexView


class TreeIndexView(IndexView):
    parent_instance = None
    parent_model = None
    parent_model_admin = None
    parent_opts = None
    parent_pk = None

    def __init__(self, model_admin):
        super(TreeIndexView, self).__init__(model_admin)

        if self.model_admin.has_parent():
            self.parent_model_admin = self.model_admin.parent
            self.parent_model = self.parent_model_admin.model
            self.parent_opts = self.parent_model._meta

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Only continue if logged in user has list permission
        if not self.permission_helper.user_can_list(request.user):
            raise PermissionDenied

        self.params = dict(request.GET.items())
        if self.model_admin.has_parent():
            parent_filter_name = self.model_admin.parent_field
            if parent_filter_name in self.params:
                self.parent_pk = unquote(self.params[parent_filter_name])
                filter_kwargs = {self.parent_opts.pk.attname: self.parent_pk}
                parent_qs = self.parent_model._default_manager.get_queryset(
                ).filter(**filter_kwargs)
                self.parent_instance = get_object_or_404(parent_qs)

        return super(TreeIndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, request=None):
        qs = super(TreeIndexView, self).get_queryset(request=request)

        if self.parent_instance is not None:
            parent_filter = {
                self.model_admin.parent_field: self.parent_instance
            }
            qs = qs.filter(**parent_filter)
        return qs

    def get_page_title(self):
        if self.parent_instance is not None:
            return str(self.parent_instance)
        return super(TreeIndexView, self).get_page_title()

    def get_parent_edit_button(self):
        if self.parent_instance is None:
            return None
        parent_button_helper_class = \
            self.parent_model_admin.get_button_helper_class()
        parent_button_helper = parent_button_helper_class(self, self.request)
        return parent_button_helper.edit_button(
            self.parent_pk,
            classnames_add=['button-secondary', 'button-small']
        )

    def get_child_filter(self, parent_pk):
        if self.has_child:
            return (
                self.child_model_admin.parent_field + '=' +
                str(parent_pk)
            )

    def get_children(self, obj):
        if self.has_child:
            return getattr(obj, self.model_admin.get_child_field())

    @cached_property
    def has_child_admin(self):
        return self.model_admin.child_instance is not None

    @cached_property
    def child_model_admin(self):
        return self.model_admin.child_instance

    @cached_property
    def has_child(self):
        return self.model_admin.has_child()

    @cached_property
    def child_name(self):
        return self.model_admin.get_child_name()

    @cached_property
    def child_name_plural(self):
        return self.model_admin.get_child_name_plural()

    @cached_property
    def child_url_helper(self):
        if self.has_child:
            return self.model_admin.child_instance.url_helper

    @property
    def breadcrumbs(self):
        model_admin = self.model_admin
        breadcrumbs = []

        while model_admin is not None:
            breadcrumbs.append((
                model_admin.url_helper.index_url,
                force_text(model_admin.model._meta.verbose_name_plural)
            ))

            if model_admin.has_parent():
                model_admin = model_admin.parent
            else:
                model_admin = None

        return reversed(breadcrumbs)
