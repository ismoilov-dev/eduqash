from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from apps.accounts.models import User

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('id', 'username', 'email', 'role', 'role_approval_status', 'is_email_verified', 'phone', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'role_approval_status', 'is_email_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'telegram_id', 'bio')
    ordering = ('-created_at',)
    actions = ['approve_selected_roles', 'reject_selected_roles']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar', 'bio')}),
        ('Role & Verification', {'fields': ('role', 'role_approval_status', 'rejection_reason', 'is_email_verified', 'telegram_id', 'google_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    @admin.action(description="Tanlangan foydalanuvchilar rolini tasdiqlash (Approve)")
    def approve_selected_roles(self, request, queryset):
        updated = queryset.update(role_approval_status='approved', rejection_reason=None)
        self.message_user(request, f"{updated} ta foydalanuvchi roli tasdiqlandi.")

    @admin.action(description="Tanlangan foydalanuvchilar rolini rad etish (Reject)")
    def reject_selected_roles(self, request, queryset):
        updated = queryset.update(role_approval_status='rejected')
        self.message_user(request, f"{updated} ta foydalanuvchi roli rad etildi.")

