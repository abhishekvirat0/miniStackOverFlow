from django.core.mail import send_mail
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Answer
from .serializers import AnswerSerializer
from questions.models import Question
from notifications.models import Notification 


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all().order_by('-created_at')
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        answer = serializer.save(author=self.request.user)
        # Notify question author
        Notification.objects.create(
            user=answer.question.author,
            message=f"{answer.author.username} answered your question '{answer.question.title}'"
        )

        send_mail(
            subject='New Answer to Your Question!',
            message=f"Hi {answer.question.author.username},\n\n{answer.author.username} has posted an answer to your "
                    f"question '{answer.question.title}'.",
            from_email=None,
            recipient_list=[answer.question.author.email],
            fail_silently=True,
        )

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        answer = self.get_object()
        if answer.question.author != request.user:
            return Response({'error': 'Only question author can accept an answer.'}, status=status.HTTP_403_FORBIDDEN)

        answer.is_accepted = True
        answer.save()

        # Notify answer author
        Notification.objects.create(
            user=answer.author,
            message=f"Your answer to '{answer.question.title}' was accepted!"
        )

        send_mail(
            subject='Your Answer was Accepted!',
            message=f"Hi {answer.author.username},\n\nYour answer to the question '{answer.question.title}' was "
                    f"accepted by the question author!",
            from_email=None,
            recipient_list=[answer.author.email],
            fail_silently=True,
        )

        return Response({'message': 'Answer accepted!'})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied('You are not allowed to edit this Answer.')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied('You are not allowed to delete this Answer.')
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        answer = self.get_object()
        answer.upvotes += 1
        answer.save()
        return Response({'status': 'answer up-voted'})

    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        answer = self.get_object()
        answer.downvotes += 1
        answer.save()
        return Response({'status': 'answer down-voted'})
