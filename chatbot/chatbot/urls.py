from django.contrib import admin
from django.urls import path, include
import apps.api.urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(apps.api.urls, namespace="api")),
]
