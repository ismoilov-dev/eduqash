from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class Conversation(BaseModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title or f"Conversation {self.id}"


class Message(BaseModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='chat/files/', max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30] if self.text else 'Attachment'}"
