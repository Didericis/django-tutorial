from rest_framework import serializers
from django.contrib.auth.models import User

from polls.models import Choice, Question, Vote

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
    votes = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name='vote-detail',
        read_only=True
    )
    class Meta:
        model = Choice
        fields = ('id', 'question', 'choice_text', 'votes', 'vote_count', 'url')

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'choice', 'user', 'created', 'url')
