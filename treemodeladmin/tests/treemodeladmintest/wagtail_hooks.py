from wagtail.contrib.modeladmin.options import (
    ModelAdminGroup,
    modeladmin_register,
)

from treemodeladmin.options import TreeModelAdmin
from treemodeladmin.tests.treemodeladmintest.models import Author, Book


class BookModelAdmin(TreeModelAdmin):
    model = Book
    parent_field = 'author'


class AuthorModelAdmin(TreeModelAdmin):
    model = Author
    child_field = 'book_set'
    child_model_admin = BookModelAdmin


@modeladmin_register
class TreeModelAdminTestGroup(ModelAdminGroup):
    menu_label = 'TreeModelAdmin Test'
    menu_icon = 'list-ul'
    items = (AuthorModelAdmin,)
