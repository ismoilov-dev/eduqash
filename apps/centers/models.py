from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class LearningCenter(BaseModel):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='centers/logos/', blank=True, null=True)
    cover = models.ImageField(upload_to='centers/covers/', blank=True, null=True)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    phone = models.CharField(max_length=50)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=512)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    work_time_start = models.TimeField(blank=True, null=True)
    work_time_end = models.TimeField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='centers'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
