from django.conf.urls import include, url

from .views import health_check

urlpatterns = [
    url(r'^(?P<key>[-\w]+)', health_check, name="object_health_check"),
]

urlpatterns = (urlpatterns, 'data_sniffer')
