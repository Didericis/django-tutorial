from rest_framework import serializers
from django.contrib.auth.models import User

from polls.models import Choice, Question

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choices = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name='choice-detail',
        read_only=True
    )
    class Meta:
        model = Question
        fields = (
            'id', 'choices', 'question_text', 'pub_date', 'private', 'url'
        )

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'question', 'choice_text', 'votes', 'url')
