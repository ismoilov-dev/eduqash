from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from apps.accounts.models import User

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('username', 'email', 'role', 'is_email_verified', 'phone', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_email_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'telegram_id')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar', 'bio')}),
        ('Role & Verification', {'fields': ('role', 'is_email_verified', 'telegram_id', 'google_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
