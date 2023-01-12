from django.test import TestCase

from treemodeladmin.options import TreeModelAdmin
from treemodeladmin.tests.treemodeladmintest.models import Author, Book


class BookHasParentModelAdmin(TreeModelAdmin):
    model = Book
    parent_field = "author"


class AuthorHasChildModelAdmin(TreeModelAdmin):
    model = Author
    child_field = "book_set"
    child_model_admin = BookHasParentModelAdmin
    index_view_extra_css = ["authors.css"]


class AuthorPlainModelAdmin(TreeModelAdmin):
    model = Author


class TestTreeModelAdmin(TestCase):
    def setUp(self):
        self.author_model_admin = AuthorHasChildModelAdmin()
        self.book_model_admin = self.author_model_admin.child_instance
        self.plain_model_admin = AuthorPlainModelAdmin()

    def test_has_child(self):
        self.assertTrue(self.author_model_admin.has_child())
        self.assertFalse(self.book_model_admin.has_child())

    def test_has_child_no_child_field(self):
        self.assertFalse(self.plain_model_admin.has_child())

    def test_has_child_no_child_model_admin(self):
        self.plain_model_admin.child_field = "book_set"
        self.assertFalse(self.plain_model_admin.has_child())

    def test_has_child_no_child_field_on_model(self):
        self.plain_model_admin.child_field = "authored_books"
        self.plain_model_admin.child_model_admin = BookHasParentModelAdmin
        self.assertFalse(self.plain_model_admin.has_child())

    def test_has_parent(self):
        self.assertFalse(self.author_model_admin.has_parent())
        self.assertTrue(self.book_model_admin.has_parent())

    def test_get_child_field(self):
        self.assertEqual(self.author_model_admin.get_child_field(), "book_set")

    def test_get_child_field_none(self):
        self.assertEqual(self.book_model_admin.get_child_field(), None)

    def test_get_child_name(self):
        self.assertEqual(self.author_model_admin.get_child_name(), "book")

    def test_get_child_name_none(self):
        self.assertEqual(self.book_model_admin.get_child_field(), None)

    def test_get_child_name_plural(self):
        self.assertEqual(
            self.author_model_admin.get_child_name_plural(), "books"
        )

    def test_get_child_name_plural_none(self):
        self.assertEqual(self.book_model_admin.get_child_field(), None)

    def test_get_parent_field(self):
        self.assertEqual(self.book_model_admin.get_parent_field(), "author")

    def test_get_parent_field_none(self):
        self.assertEqual(self.author_model_admin.get_parent_field(), None)

    def test_get_index_view_extra_css(self):
        self.assertEqual(
            self.author_model_admin.get_index_view_extra_css(),
            [
                "treemodeladmin/css/index.css",
                "authors.css",
            ],
        )

    def test_get_index_view_extra_css_none(self):
        self.assertEqual(
            self.plain_model_admin.get_index_view_extra_css(),
            [
                "treemodeladmin/css/index.css",
            ],
        )

    def test_get_admin_urls_for_registration_child(self):
        self.assertGreaterEqual(
            len(self.author_model_admin.get_admin_urls_for_registration()), 8
        )

    def test_get_admin_urls_for_registration_no_child(self):
        self.assertGreaterEqual(
            len(self.book_model_admin.get_admin_urls_for_registration()), 4
        )
