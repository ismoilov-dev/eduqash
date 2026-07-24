from rest_framework.routers import DefaultRouter
from apps.chat.views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='chat-messages')
router.register(r'conversations', ConversationViewSet, basename='chat-conversations')

urlpatterns = router.urls
