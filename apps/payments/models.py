import uuid
from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.courses.models import Course


class PromoCode(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    valid_until = models.DateTimeField(blank=True, null=True)
    usage_limit = models.PositiveIntegerField(default=100)
    times_used = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} (-{self.discount_percent}%)"


class Payment(BaseModel):
    PROVIDER_CHOICES = (
        ('payme', 'Payme'),
        ('click', 'Click'),
        ('uzum', 'Uzum Bank'),
        ('fake', 'Fake Payment (Dev)'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='fake')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.transaction_id} - {self.user.username} ({self.status})"
