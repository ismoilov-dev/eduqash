from rest_framework import viewsets, permissions, status, parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.chat.models import Conversation, Message
from apps.chat.serializers import (
    ConversationSerializer,
    MessageSerializer,
    CreateConversationSerializer,
)
from apps.accounts.models import User


@extend_schema_view(
    list=extend_schema(summary="Foydalanuvchining barcha chat suhbatlari ro'yxatini ko'rish"),
    retrieve=extend_schema(summary="Chat suhbati tafsilotlarini ko'rish"),
    update=extend_schema(summary="Chat suhbatini to'liq tahrirlash"),
    partial_update=extend_schema(summary="Chat suhbatini qisman tahrirlash"),
    destroy=extend_schema(summary="Chat suhbatini o'chirish"),
)
@extend_schema(tags=['Chat'])
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Conversation.objects.none()
        return self.request.user.conversations.filter(is_active=True)

    @extend_schema(summary="Yangi chat suhbatini boshlash", request=CreateConversationSerializer, responses={201: ConversationSerializer})
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


@extend_schema_view(
    list=extend_schema(summary="Suhbatdagi eski xabarlar tarixini ko'rish (?conversation=<id>)"),
    create=extend_schema(summary="Chatga xabar yoki fayl yuborish"),
    retrieve=extend_schema(summary="Xabar tafsilotlarini ko'rish"),
    update=extend_schema(summary="Xabarni to'liq tahrirlash"),
    partial_update=extend_schema(summary="Xabarni qisman tahrirlash"),
    destroy=extend_schema(summary="Xabarni o'chirish"),
)
@extend_schema(tags=['Chat'])
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Message.objects.none()
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id, conversation__participants=self.request.user)
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
