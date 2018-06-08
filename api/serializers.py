from rest_framework import serializers
from django.contrib.auth.models import User

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name='snippet-detail',
        read_only=True
    )
    votes = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name='vote-detail',
        read_only=True
    )

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets', 'votes')
