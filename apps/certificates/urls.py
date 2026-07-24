from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.certificates.views import (
    CertificateViewSet,
    IssueCertificateView,
    VerifyCertificateView,
)

router = DefaultRouter()
router.register(r'', CertificateViewSet, basename='certificates')

urlpatterns = [
    path('issue/', IssueCertificateView.as_view(), name='certificates_issue'),
    path('verify/<uuid:unique_id>/', VerifyCertificateView.as_view(), name='certificates_verify'),
] + router.urls
