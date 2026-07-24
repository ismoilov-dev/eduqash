from rest_framework.routers import DefaultRouter
from apps.reviews.views import ReviewViewSet, ReviewReportViewSet

router = DefaultRouter()
router.register(r'reports', ReviewReportViewSet, basename='review-reports')
router.register(r'', ReviewViewSet, basename='reviews')

urlpatterns = router.urls
