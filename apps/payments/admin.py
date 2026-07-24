from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.payments.models import Payment, PromoCode


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ('transaction_id', 'user', 'course', 'amount', 'provider', 'status', 'created_at')
    list_filter = ('provider', 'status', 'created_at')
    search_fields = ('transaction_id', 'user__username', 'user__email')
    ordering = ('-created_at',)


@admin.register(PromoCode)
class PromoCodeAdmin(ModelAdmin):
    list_display = ('code', 'discount_percent', 'usage_limit', 'times_used', 'valid_until', 'is_active')
    list_filter = ('is_active', 'valid_until')
    search_fields = ('code',)
