from django.test import TestCase

from wagtail.test.utils import WagtailTestUtils

from treemodeladmin.tests.treemodeladmintest.models import Author, Book


class TestAuthorIndexView(TestCase, WagtailTestUtils):
    fixtures = ["treemodeladmin_test.json"]

    def setUp(self):
        self.user = self.login()

    def get(self, **params):
        return self.client.get("/admin/treemodeladmintest/author/", params)

    def test_author_listing(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 4)

    def test_explore_link(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Explore J. R. R. Tolkien's books")
        self.assertContains(response, "/book/?author=1")

    def test_add_child_link(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add a J. R. Hartley book")
        self.assertContains(response, "/book/create/?author=4")

    def test_has_child_admin(self):
        response = self.get()
        self.assertTrue(response.context["view"].has_child_admin)

    def test_breadcrumbs(self):
        resposne = self.get()
        self.assertEqual(
            list(resposne.context["view"].breadcrumbs),
            [("/admin/treemodeladmintest/author/", "authors")],
        )

    def test_get_context_data(self):
        response = self.get()
        self.assertFalse(response.context["user_can_edit"])


class TestAuthorCreateView(TestCase, WagtailTestUtils):
    fixtures = ["treemodeladmin_test.json"]

    def setUp(self):
        self.user = self.login()

    def post(self, post_data):
        return self.client.post(
            "/admin/treemodeladmintest/author/create/", post_data
        )

    def test_create_redirects_to_plain_index(self):
        response = self.post({"name": "P. G. Wodehouse"})

        # Should redirect back to
        self.assertRedirects(response, "/admin/treemodeladmintest/author/")


class TestBookIndexView(TestCase, WagtailTestUtils):
    fixtures = ["treemodeladmin_test.json"]

    def setUp(self):
        self.user = self.login()

    def get(self, **params):
        return self.client.get("/admin/treemodeladmintest/book/", params)

    def test_book_listing(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 4)

    def test_book_listing_filtered(self):
        response = self.get(author=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 2)
        self.assertEqual(
            response.context["view"].get_page_title(), "J. R. R. Tolkien"
        )

    def test_book_listing_add_link_filtered(self):
        response = self.get(author=1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/book/create/?author=1")

    def test_has_child_admin(self):
        response = self.get(author=1)
        self.assertTrue(response.context["view"].has_child_admin)

    def test_book_listing_parent_edit_link_filtered(self):
        response = self.get(author=1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/author/edit/1")

    def test_breadcrumbs(self):
        resposne = self.get()
        self.assertEqual(
            list(resposne.context["view"].breadcrumbs),
            [
                ("/admin/treemodeladmintest/author/", "authors"),
                ("/admin/treemodeladmintest/book/", "books"),
            ],
        )

    def test_breadcrumbs_with_parent(self):
        resposne = self.get(author=1)
        self.assertEqual(
            list(resposne.context["view"].breadcrumbs),
            [
                ("/admin/treemodeladmintest/author/", "authors"),
                (
                    "/admin/treemodeladmintest/book/?author=1",
                    "J. R. R. Tolkien",
                ),
            ],
        )

    def test_get_context_data(self):
        response = self.get(author=1)
        self.assertTrue(response.context["user_can_edit"])


class TestBookCreateView(TestCase, WagtailTestUtils):
    fixtures = ["treemodeladmin_test.json"]

    def setUp(self):
        self.user = self.login()

    def get(self, **params):
        return self.client.get(
            "/admin/treemodeladmintest/book/create/", params
        )

    def post(self, post_data):
        return self.client.post(
            "/admin/treemodeladmintest/book/create/", post_data
        )

    def test_book_creation_with_initial_author(self):
        response = self.get(author=1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="1" selected')

    def test_create_redirects_to_author(self):
        response = self.post({"title": "The Silmarilian", "author": 1})

        # Should redirect back to
        self.assertRedirects(
            response, "/admin/treemodeladmintest/book/?author=1"
        )


class TestBookEditView(TestCase, WagtailTestUtils):
    fixtures = ["treemodeladmin_test.json"]

    def setUp(self):
        self.user = self.login()

    def post(self, book_id, post_data):
        return self.client.post(
            f"/admin/treemodeladmintest/book/edit/{book_id}/",
            post_data,
        )

    def test_create_redirects_to_author(self):
        response = self.post(
            1, {"title": "The Lord of the Rings", "author": 1}
        )
        self.assertRedirects(
            response, "/admin/treemodeladmintest/book/?author=1"
        )


class TestBookDeleteView(TestCase, WagtailTestUtils):
    fixtures = ["treemodeladmin_test.json"]

    def setUp(self):
        self.login()

    def post(self, book_id):
        return self.client.post(
            f"/admin/treemodeladmintest/book/delete/{book_id}/"
        )

    def test_post(self):
        response = self.post(2)
        self.assertRedirects(
            response, "/admin/treemodeladmintest/book/?author=1"
        )
        self.assertFalse(Book.objects.filter(id=2).exists())


class TestAuthorDeleteView(TestCase, WagtailTestUtils):
    fixtures = ["treemodeladmin_test.json"]

    def setUp(self):
        self.login()

    def post(self, author_id):
        return self.client.post(
            f"/admin/treemodeladmintest/author/delete/{author_id}/"
        )

    def test_post_with_dependent_object(self):
        response = self.post(1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "'J. R. R. Tolkien' is currently referenced by other objects",
        )
        self.assertContains(
            response, "<li><b>Book:</b> The Lord of the Rings</li>"
        )
        self.assertTrue(Author.objects.filter(id=1).exists())

    def test_post_without_dependent_object(self):
        response = self.post(4)
        self.assertRedirects(response, "/admin/treemodeladmintest/author/")
        self.assertFalse(Author.objects.filter(id=4).exists())


class TestVolumeIndexView(TestCase, WagtailTestUtils):
    fixtures = ["treemodeladmin_test.json"]

    def setUp(self):
        self.user = self.login()

    def get(self, **params):
        return self.client.get("/admin/treemodeladmintest/volume/", params)

    def test_has_child_admin(self):
        response = self.get()
        self.assertFalse(response.context["view"].has_child_admin)

    def test_volume_listing_filtered(self):
        response = self.get(book=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 1)
        self.assertEqual(
            response.context["view"].get_page_title(), "The Lord of the Rings"
        )

    def test_breadcrumbs_with_parents(self):
        resposne = self.get(book=1)
        self.assertEqual(
            list(resposne.context["view"].breadcrumbs),
            [
                ("/admin/treemodeladmintest/author/", "authors"),
                (
                    "/admin/treemodeladmintest/book/?author=1",
                    "J. R. R. Tolkien",
                ),
                (
                    "/admin/treemodeladmintest/volume/?book=1",
                    "The Lord of the Rings",
                ),
            ],
        )
