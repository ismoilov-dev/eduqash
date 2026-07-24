from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.certificates.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(ModelAdmin):
    list_display = ('unique_id', 'user', 'course', 'exam', 'title', 'issue_date')
    list_filter = ('issue_date',)
    search_fields = ('unique_id', 'user__username', 'title')
    ordering = ('-issue_date',)
