from wagtail_modeladmin.options import ModelAdminGroup, modeladmin_register

from treemodeladmin.options import TreeModelAdmin
from treemodeladmin.tests.treemodeladmintest.models import Author, Book, Volume


class VolumeModelAdmin(TreeModelAdmin):
    model = Volume
    parent_field = "book"


class BookModelAdmin(TreeModelAdmin):
    model = Book
    child_field = "volume_set"
    child_model_admin = VolumeModelAdmin
    parent_field = "author"


class AuthorModelAdmin(TreeModelAdmin):
    model = Author
    child_field = "book_set"
    child_model_admin = BookModelAdmin


@modeladmin_register
class TreeModelAdminTestGroup(ModelAdminGroup):
    menu_label = "TreeModelAdmin Test"
    menu_icon = "list-ul"
    items = (AuthorModelAdmin,)
