from rest_framework import viewsets, permissions, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


@extend_schema_view(
    list=extend_schema(summary="Foydalanuvchiga kelgan bildirishnomalar ro'yxati"),
    retrieve=extend_schema(summary="Bildirishnoma tafsilotini ko'rish"),
    update=extend_schema(summary="Bildirishnomani tahrirlash"),
    partial_update=extend_schema(summary="Bildirishnomani qisman tahrirlash"),
    destroy=extend_schema(summary="Bildirishnomani o'chirish"),
)
@extend_schema(tags=['Notifications'])
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Notification.objects.none()
        user = self.request.user
        if user.role in ['super_admin', 'admin']:
            return Notification.objects.filter(is_active=True)
        return Notification.objects.filter(user=user, is_active=True)

    def perform_create(self, serializer):
        if 'user' not in serializer.validated_data:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    @extend_schema(summary="Bitta bildirishnomani o'qilgan deb belgilash", request=None)
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'}, status=status.HTTP_200_OK)

    @extend_schema(summary="Barcha bildirishnomalarni o'qilgan deb belgilash", request=None)
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all notifications marked as read'}, status=status.HTTP_200_OK)
