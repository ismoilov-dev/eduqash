from rest_framework.routers import DefaultRouter
from apps.centers.views import LearningCenterViewSet

# Learning Centers API Endpoints (Frontend uchun)
# Base path: /centers/
# - GET /centers/ : O'quv markazlari ro'yxati (Params: ?search=...&owner=...&ordering=rating)
# - POST /centers/ : Yangi markaz qo'shish (Center Owner / Admin)
# - GET /centers/{id}/ : Markaz haqida batafsil ma'lumot
# - PUT/PATCH /centers/{id}/ : Markazni tahrirlash (Owner / Admin)
# - DELETE /centers/{id}/ : Markazni o'chirish (Owner / Admin)
router = DefaultRouter()
router.register(r'', LearningCenterViewSet, basename='centers')

urlpatterns = router.urls
