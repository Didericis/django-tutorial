from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'choices', views.ChoiceViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'votes', views.VoteViewSet)
