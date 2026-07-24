import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import BaseModel


class User(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('teacher', 'Teacher'),
        ('center_owner', 'Learning Center Owner'),
        ('student', 'Student'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    password_reset_code = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
