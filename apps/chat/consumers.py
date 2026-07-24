import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.chat.models import Conversation, Message
from apps.accounts.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope.get('user')

        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        # Check conversation membership
        is_member = await self.check_membership(self.conversation_id, self.user)
        if not is_member:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message', '')

        if not message_text:
            return

        # Save message to database
        saved_msg = await self.save_message(self.conversation_id, self.user, message_text)

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': str(saved_msg.id),
                'sender_id': str(self.user.id),
                'sender_username': self.user.username,
                'message': message_text,
                'created_at': saved_msg.created_at.isoformat()
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def check_membership(self, conversation_id, user):
        try:
            conv = Conversation.objects.get(id=conversation_id)
            return conv.participants.filter(id=user.id).exists()
        except Exception:
            return False

    @database_sync_to_async
    def save_message(self, conversation_id, user, text):
        conv = Conversation.objects.get(id=conversation_id)
        msg = Message.objects.create(
            conversation=conv,
            sender=user,
            text=text
        )
        conv.save()  # update updated_at timestamp
        return msg
