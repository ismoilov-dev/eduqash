from rest_framework import serializers
from apps.chat.models import Conversation, Message
from apps.accounts.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender_details = UserSerializer(source='sender', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender', 'created_at', 'updated_at')


from drf_spectacular.utils import extend_schema_field


class ConversationSerializer(serializers.ModelSerializer):
    participants_details = UserSerializer(source='participants', many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    @extend_schema_field(MessageSerializer)
    def get_last_message(self, obj):
        last = obj.messages.order_by('-created_at').first()
        return MessageSerializer(last).data if last else None


class CreateConversationSerializer(serializers.Serializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField()
    )
    title = serializers.CharField(required=False, allow_blank=True)
