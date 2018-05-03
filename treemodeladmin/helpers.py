from wagtail.contrib.modeladmin.helpers import ButtonHelper


class TreeButtonHelper(ButtonHelper):

    def add_button(self, classnames_add=None, classnames_exclude=None):
        return super(TreeButtonHelper, self).add_button(
            classnames_add=['button-small']
        )
