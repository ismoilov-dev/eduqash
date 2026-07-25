from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='frontend-home'),
    path('admin/', admin.site.urls),

    # OpenAPI 3 Schema & UI
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-docs'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Application endpoints
    path('auth/', include('apps.accounts.urls')),
    path('centers/', include('apps.centers.urls')),
    path('courses/', include('apps.courses.urls')),
    path('exams/', include('apps.exams.urls')),
    path('quizzes/', include('apps.quizzes.urls')),
    path('ai/', include('apps.ai_assistant.urls')),
    path('payments/', include('apps.payments.urls')),
    path('certificates/', include('apps.certificates.urls')),
    path('chat/', include('apps.chat.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
