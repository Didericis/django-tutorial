from rest_framework import serializers
from django.contrib.auth.models import User

from polls.models import Choice, Question

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date', 'private', 'url')

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'votes', 'url')
