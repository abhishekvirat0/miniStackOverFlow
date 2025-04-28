from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Only authenticated users can create/update/delete
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'tags']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.get('tags')
        if tags:
            queryset = queryset.filter(tags__icontains=tags)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied('You are not allowed to edit this question.')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied('You are not allowed to delete this question.')
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        question = self.get_object()
        question.upvotes += 1
        question.save()
        return Response({'status': 'question up-voted'})

    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        question = self.get_object()
        question.downvotes += 1
        question.save()
        return Response({'status': 'question down-voted'})
