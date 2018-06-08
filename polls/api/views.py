from rest_framework import viewsets

from .serializers import ChoiceSerializer, QuestionSerializer, VoteSerializer
from polls.models import Choice, Question, Vote

# TODO: API related things should probably move
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer 
