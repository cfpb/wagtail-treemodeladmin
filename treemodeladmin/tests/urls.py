from wagtail.admin import urls as wagtailadmin_urls


try:
    from django.urls import include, re_path
except ImportError:
    from django.conf.urls import include
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(r"^admin/", include(wagtailadmin_urls)),
]
