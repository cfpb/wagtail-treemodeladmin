from django.conf.urls import include, url

import wagtail


if wagtail.VERSION >= (2, 0):
    from wagtail.admin import urls as wagtailadmin_urls
else:
    from wagtail.wagtailadmin import urls as wagtailadmin_urls


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
]
