from rest_framework import serializers
from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Answer
        fields = ['id', 'question', 'body', 'author_username', 'created_at', 'updated_at', 'is_accepted', 'upvotes',
                  'downvotes']
        read_only_fields = ['author_username', 'created_at', 'updated_at', 'is_accepted', 'upvotes', 'downvotes']
