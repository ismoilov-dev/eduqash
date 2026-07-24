from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class Notification(BaseModel):
    TYPE_CHOICES = (
        ('system', 'System'),
        ('email', 'Email'),
        ('telegram', 'Telegram'),
        ('course', 'Course Update'),
        ('exam', 'Exam Result'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification to {self.user.username}: {self.title}"
