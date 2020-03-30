from django.conf.urls import include, url

from wagtail.admin import urls as wagtailadmin_urls


urlpatterns = [
    url(r"^admin/", include(wagtailadmin_urls)),
]
