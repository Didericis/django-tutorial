from django.urls import path 
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from polls.api.urls import router as polls_api_router 
from snippets.api.urls import router as snippets_api_router
from . import views

schema_view = get_schema_view(title='MySite API')

router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.registry.extend(polls_api_router.registry)
router.registry.extend(snippets_api_router.registry)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^schema', schema_view),
    url(r'^', include(router.urls))
]
