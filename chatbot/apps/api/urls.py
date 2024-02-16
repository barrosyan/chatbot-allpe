from rest_framework import routers
from django.urls import path, include
from .views.prompt import ChatAPIViewSet

router = routers.DefaultRouter()
router.register(r'', ChatAPIViewSet, basename="chat")

app_name = "api"
urlpatterns = [
    path("", include(router.urls))
]