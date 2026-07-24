from rest_framework import viewsets, permissions, filters, parsers
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.centers.models import LearningCenter
from apps.centers.serializers import LearningCenterSerializer
from apps.core.permissions import IsOwnerOrReadOnly, IsCenterOwner


@extend_schema_view(
    list=extend_schema(summary="O'quv markazlari ro'yxatini ko'rish"),
    create=extend_schema(summary="Yangi o'quv markazi qo'shish (Markaz Egasi/Admin)"),
    retrieve=extend_schema(summary="O'quv markazi ma'lumotlarini ko'rish"),
    update=extend_schema(summary="O'quv markazini to'liq tahrirlash"),
    partial_update=extend_schema(summary="O'quv markazini qisman tahrirlash"),
    destroy=extend_schema(summary="O'quv markazini o'chirish"),
)
@extend_schema(tags=['Centers'])
class LearningCenterViewSet(viewsets.ModelViewSet):
    queryset = LearningCenter.objects.filter(is_active=True)
    serializer_class = LearningCenterSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'address']
    filterset_fields = ['owner']
    ordering_fields = ['rating', 'created_at']

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), IsCenterOwner()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]
