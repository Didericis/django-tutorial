from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'snippets', views.SnippetViewSet)
