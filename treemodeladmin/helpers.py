from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.helpers import AdminURLHelper


class TreeAdminURLHelper(AdminURLHelper):

    def get_create_url_with_parent(self, parent_field, parent_pk):
        return '{create_url}?{parent_field}={parent_pk}'.format(
            create_url=self.create_url,
            parent_field=parent_field,
            parent_pk=parent_pk
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
