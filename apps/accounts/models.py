from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from apps.core.models import BaseModel


class UserManager(BaseUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'super_admin')
        extra_fields.setdefault('role_approval_status', 'approved')
        extra_fields.setdefault('is_email_verified', True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('teacher', 'Teacher'),
        ('center_owner', 'Learning Center Owner'),
        ('student', 'Student'),
    )

    ROLE_APPROVAL_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    role_approval_status = models.CharField(
        max_length=20, 
        choices=ROLE_APPROVAL_STATUS_CHOICES, 
        default='pending'
    )
    rejection_reason = models.TextField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', max_length=500, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    password_reset_code = models.CharField(max_length=6, blank=True, null=True)

    objects = UserManager()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'super_admin'
            self.role_approval_status = 'approved'
            self.is_email_verified = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
