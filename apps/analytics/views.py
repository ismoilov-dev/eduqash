from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema

from apps.accounts.models import User
from apps.courses.models import Course
from apps.centers.models import LearningCenter
from apps.exams.models import ExamAttempt
from apps.payments.models import Payment
from apps.certificates.models import Certificate
from apps.core.permissions import IsAdmin


@extend_schema(tags=['Analytics'])
class DashboardOverviewView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @extend_schema(summary="Admin paneli uchun umumiy platforma analitikasi", responses={200: dict})
    def get(self, request):
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        # Users counts
        total_users = User.objects.count()
        total_students = User.objects.filter(role='student').count()
        total_teachers = User.objects.filter(role='teacher').count()
        total_center_owners = User.objects.filter(role='center_owner').count()

        # Platform stats
        total_centers = LearningCenter.objects.filter(is_active=True).count()
        total_courses = Course.objects.filter(is_active=True).count()
        completed_exams = ExamAttempt.objects.filter(is_completed=True).count()
        issued_certificates = Certificate.objects.count()

        # Revenue aggregations
        revenue_all_time = Payment.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0.0
        revenue_today = Payment.objects.filter(status='paid', created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0.0
        revenue_week = Payment.objects.filter(status='paid', created_at__gte=week_ago).aggregate(total=Sum('amount'))['total'] or 0.0
        revenue_month = Payment.objects.filter(status='paid', created_at__gte=month_ago).aggregate(total=Sum('amount'))['total'] or 0.0

        return Response({
            'users': {
                'total': total_users,
                'students': total_students,
                'teachers': total_teachers,
                'center_owners': total_center_owners,
            },
            'platform': {
                'total_centers': total_centers,
                'total_courses': total_courses,
                'completed_exams': completed_exams,
                'issued_certificates': issued_certificates,
            },
            'revenue': {
                'today': float(revenue_today),
                'weekly': float(revenue_week),
                'monthly': float(revenue_month),
                'all_time': float(revenue_all_time),
            }
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Analytics'])
class RevenueAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @extend_schema(summary="Daromadlar va to'lov usullari statistikasi", responses={200: dict})
    def get(self, request):
        by_provider = Payment.objects.values('provider').annotate(
            total_revenue=Sum('amount'),
            payments_count=Count('id')
        )
        by_status = Payment.objects.values('status').annotate(
            count=Count('id')
        )

        return Response({
            'by_provider': list(by_provider),
            'by_status': list(by_status),
        }, status=status.HTTP_200_OK)
