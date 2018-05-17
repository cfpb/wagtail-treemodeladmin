from django.contrib.admin.utils import unquote
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.functional import cached_property

from wagtail.contrib.modeladmin.views import IndexView, CreateView


class TreeViewParentMixin(object):

    @cached_property
    def parent_model_admin(self):
        if self.model_admin.has_parent():
            return self.model_admin.parent

    @cached_property
    def parent_model(self):
        if self.model_admin.has_parent():
            return self.parent_model_admin.model

    @cached_property
    def parent_opts(self):
        if self.model_admin.has_parent():
            return self.parent_model._meta

    @cached_property
    def parent_instance(self):
        if self.model_admin.has_parent():
            params = dict(self.request.GET.items())
            if self.model_admin.parent_field in params:
                parent_pk = unquote(params[self.model_admin.parent_field])
                filter_kwargs = {self.parent_opts.pk.attname: parent_pk}
                parent_qs = self.parent_model._default_manager.get_queryset(
                ).filter(**filter_kwargs)
                return get_object_or_404(parent_qs)


class TreeIndexView(TreeViewParentMixin, IndexView):

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
            self.parent_instance.pk,
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

    def get_add_button_with_parent(self):
        if self.parent_instance is not None:
            return self.button_helper.get_add_button_with_parent(
                self.model_admin.parent_field, self.parent_instance.pk
            )
        return self.button_helper.add_button

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


class TreeCreateView(TreeViewParentMixin, CreateView):

    def get_initial(self):
        initial = super(TreeCreateView, self).get_initial()
        if self.parent_instance is not None:
            initial[self.model_admin.parent_field] = self.parent_instance.pk
        return initial
