from django.contrib.admin.utils import unquote
from django.db import models
from django.shortcuts import get_object_or_404, redirect
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from wagtail.admin import messages

from wagtail_modeladmin.views import (
    CreateView,
    DeleteView,
    EditView,
    IndexView,
)


class TreeViewParentMixin:
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
            if getattr(self, "instance", None) is not None:
                return getattr(self.instance, self.model_admin.parent_field)

            if self.request.method == "POST":
                params = dict(self.request.POST.items())
            else:
                params = dict(self.request.GET.items())

            if self.model_admin.parent_field in params:
                parent_pk = unquote(params[self.model_admin.parent_field])
                filter_kwargs = {self.parent_opts.pk.attname: parent_pk}
                parent_qs = (
                    self.parent_model._default_manager.get_queryset().filter(  # noqa
                        **filter_kwargs
                    )
                )
                return get_object_or_404(parent_qs)

    @property
    def breadcrumbs(self):
        parent_instance = self.parent_instance
        model_admin = self.model_admin

        breadcrumbs = []

        while model_admin is not None:
            breadcrumbs.append(
                model_admin.url_helper.crumb(
                    parent_field=model_admin.parent_field,
                    parent_instance=parent_instance,
                    specific_instance=parent_instance,
                )
            )

            if model_admin.has_parent():
                model_admin = model_admin.parent
                parent_instance = getattr(
                    parent_instance, model_admin.parent_field, None
                )
            else:
                model_admin = None

        return reversed(breadcrumbs)


class TreeIndexView(TreeViewParentMixin, IndexView):
    def get_queryset(self, request=None):
        qs = super().get_queryset(request=request)

        if self.parent_instance is not None:
            parent_filter = {
                self.model_admin.parent_field: self.parent_instance
            }
            qs = qs.filter(**parent_filter)
        return qs

    def get_page_title(self):
        if self.parent_instance is not None:
            return str(self.parent_instance)
        return super().get_page_title()

    def get_parent_edit_button(self):
        if self.parent_instance is None:
            return None
        parent_button_helper_class = (
            self.parent_model_admin.get_button_helper_class()
        )
        parent_button_helper = parent_button_helper_class(
            self.parent_model_admin, self.request
        )
        return parent_button_helper.edit_button(
            self.parent_instance.pk,
            classnames_add=["button-small"],
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

    def get_context_data(self, **kwargs):
        user = self.request.user
        user_can_edit = (
            self.permission_helper.user_can_edit_obj(
                user, self.parent_instance
            )
            if self.parent_instance is not None
            else False
        )
        context = {"user_can_edit": user_can_edit}
        return super().get_context_data(**context)

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


class TreeModelFormMixin(TreeViewParentMixin):
    def get_success_url(self):
        if self.parent_instance is not None:
            return self.url_helper.get_index_url_with_parent(
                self.model_admin.parent_field, self.parent_instance.pk
            )
        return self.index_url


class TreeCreateView(TreeModelFormMixin, CreateView):
    def get_initial(self):
        initial = super().get_initial()
        if self.parent_instance is not None:
            initial[self.model_admin.parent_field] = self.parent_instance.pk
        return initial


class TreeEditView(TreeModelFormMixin, EditView):
    pass


class TreeDeleteView(TreeViewParentMixin, DeleteView):
    def post(self, request, *args, **kwargs):
        # Unfortunately, ModelAdmin doesn't provide a good way to override the
        # redirect(self.index_url) like the edit/create views. So this is
        # copied directly from modeladmin.views.DeleteView.
        try:
            if self.parent_instance is not None:
                index_url = self.url_helper.get_index_url_with_parent(
                    self.model_admin.parent_field, self.parent_instance.pk
                )
            else:
                index_url = self.index_url

            msg = _("{model} '{instance}' deleted.").format(
                model=self.verbose_name, instance=self.instance
            )
            self.delete_instance()
            messages.success(request, msg)

            return redirect(index_url)
        except models.ProtectedError:
            linked_objects = []
            fields = self.model._meta.fields_map.values()
            fields = (
                obj
                for obj in fields
                if not isinstance(
                    obj.field, models.fields.related.ManyToManyField
                )
            )
            for rel in fields:
                if rel.on_delete == models.PROTECT:
                    qs = getattr(self.instance, rel.get_accessor_name())
                    for obj in qs.all():
                        linked_objects.append(obj)
            context = self.get_context_data(
                protected_error=True, linked_objects=linked_objects
            )

        return self.render_to_response(context)
