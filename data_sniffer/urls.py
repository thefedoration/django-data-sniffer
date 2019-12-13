from django.conf.urls import include, url
from django.conf import settings

from .views import health_check

if settings.DATA_SNIFFER_ENABLED:
    urlpatterns = [
        url(r'^(?P<key>[-\w]+)', health_check, name="object_health_check"),
    ]
else:
    urlpatterns = []
