from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from apps.reviews.models import Review, ReviewReport
from apps.reviews.serializers import ReviewSerializer, ReviewReportSerializer
from apps.core.permissions import IsOwnerOrReadOnly, IsAdmin


@extend_schema(tags=['Reviews'])
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.filter(is_active=True)
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'center', 'teacher', 'rating']
    ordering_fields = ['rating', 'likes_count', 'created_at']

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]

    @extend_schema(tags=['Reviews'], request=None)
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        review = self.get_object()
        review.likes_count += 1
        review.save()
        return Response({'likes_count': review.likes_count}, status=status.HTTP_200_OK)

    @extend_schema(tags=['Reviews'], request=None)
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
        review = self.get_object()
        review.dislikes_count += 1
        review.save()
        return Response({'dislikes_count': review.dislikes_count}, status=status.HTTP_200_OK)


@extend_schema(tags=['Reviews'])
class ReviewReportViewSet(viewsets.ModelViewSet):
    queryset = ReviewReport.objects.all()
    serializer_class = ReviewReportSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdmin()]
