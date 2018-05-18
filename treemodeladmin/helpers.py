from django.contrib.admin.utils import quote
from django.utils.encoding import force_text

from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper


class TreeAdminURLHelper(AdminURLHelper):

    def get_create_url_with_parent(self, parent_field, parent_pk):
        return '{create_url}?{parent_field}={parent_pk}'.format(
            create_url=self.create_url,
            parent_field=parent_field,
            parent_pk=quote(parent_pk)
        )

    def get_index_url_with_parent(self, parent_field, parent_pk):
        return '{index_url}?{parent_field}={parent_pk}'.format(
            index_url=self.index_url,
            parent_field=parent_field,
            parent_pk=quote(parent_pk)
        )

    def crumb(self, parent_field=None, parent_instance=None):
        if parent_field is not None and parent_instance is not None:
            index_url = self.get_index_url_with_parent(
                parent_field,
                parent_instance.pk
            )
        else:
            index_url = self.index_url

        return (
            index_url,
            force_text(self.opts.verbose_name_plural)
        )


class TreeButtonHelper(ButtonHelper):

    def add_button(self, classnames_add=None, classnames_exclude=None):
        return super(TreeButtonHelper, self).add_button(
            classnames_add=['button-small']
        )

    def get_add_button_with_parent(self, parent_field, parent_pk,
                                   classnames_add=None,
                                   classnames_exclude=None):
        add_button = self.add_button(classnames_add=classnames_add,
                                     classnames_exclude=classnames_exclude)
        add_button['url'] = self.url_helper.get_create_url_with_parent(
            parent_field,
            parent_pk
        )
        return add_button
