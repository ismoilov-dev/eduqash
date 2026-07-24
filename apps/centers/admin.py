from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.centers.models import LearningCenter


@admin.register(LearningCenter)
class LearningCenterAdmin(ModelAdmin):
    list_display = ('id', 'name', 'owner', 'rating', 'phone', 'address', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'address', 'phone', 'telegram')
    ordering = ('-created_at',)
