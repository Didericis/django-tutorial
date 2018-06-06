from rest_framework import viewsets

from .serializers import ChoiceSerializer, QuestionSerializer
from polls.models import Choice, Question

# TODO: API related things should probably move
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
