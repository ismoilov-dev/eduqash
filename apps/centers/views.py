from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from apps.centers.models import LearningCenter
from apps.centers.serializers import LearningCenterSerializer
from apps.core.permissions import IsOwnerOrReadOnly, IsCenterOwner


@extend_schema(tags=['Centers'])
class LearningCenterViewSet(viewsets.ModelViewSet):
    queryset = LearningCenter.objects.filter(is_active=True)
    serializer_class = LearningCenterSerializer
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
