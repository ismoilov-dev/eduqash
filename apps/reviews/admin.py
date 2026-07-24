from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.reviews.models import Review, ReviewReport


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('id', 'user', 'rating', 'course', 'center', 'teacher', 'likes_count', 'dislikes_count', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'comment')


@admin.register(ReviewReport)
class ReviewReportAdmin(ModelAdmin):
    list_display = ('review', 'reported_by', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('reported_by__username', 'reason')
