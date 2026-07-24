from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.chat.models import Conversation, Message
from apps.chat.serializers import (
    ConversationSerializer,
    MessageSerializer,
    CreateConversationSerializer,
)
from apps.accounts.models import User


@extend_schema(tags=['Chat'])
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Conversation.objects.none()
        return self.request.user.conversations.filter(is_active=True)

    @extend_schema(tags=['Chat'], request=CreateConversationSerializer)
    def create(self, request, *args, **kwargs):
        serializer = CreateConversationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        participant_ids = serializer.validated_data['participant_ids']
        title = serializer.validated_data.get('title', '')

        users = User.objects.filter(id__in=participant_ids)
        conv = Conversation.objects.create(title=title)
        conv.participants.add(request.user)
        for u in users:
            conv.participants.add(u)

        return Response(ConversationSerializer(conv).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Chat'])
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Message.objects.none()
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id, conversation__participants=self.request.user)
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
