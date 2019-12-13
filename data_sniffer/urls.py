from django.conf.urls import include, url
from django.conf import settings

from .views import data_sniffer_health_check

if settings.DATA_SNIFFER_ENABLED:
    urlpatterns = [
        url(r'^(?P<key>[-\w]+)', data_sniffer_health_check, name="data_sniffer_health_check"),
    ]
else:
    urlpatterns = []
