from django.conf.urls import include, url


try:
    from wagtail.admin import urls as wagtailadmin_urls
except ImportError:
    from wagtail.wagtailadmin import urls as wagtailadmin_urls


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
]
