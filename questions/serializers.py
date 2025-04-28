from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'tags', 'created_at', 'updated_at', 'author_username', 'upvotes', 'downvotes']
        read_only_fields = ['author_username', 'created_at', 'updated_at', 'upvotes', 'downvotes']
