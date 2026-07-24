from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from apps.chat.models import Conversation, Message


class MessageInline(TabularInline):
    model = Message
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title', 'participants__username')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('conversation', 'sender', 'text', 'created_at')
    search_fields = ('sender__username', 'text')
    list_filter = ('created_at',)
