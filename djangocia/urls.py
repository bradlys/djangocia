from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


urlpatterns = [
    url(r'^api/', include('cia.urls')),
    url(r'^admin/', admin.site.urls),
]
