from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.certificates.models import Certificate
from apps.certificates.serializers import (
    CertificateSerializer,
    IssueCertificateSerializer,
)
from apps.certificates.generator import CertificateGenerator
from apps.accounts.models import User
from apps.courses.models import Course
from apps.exams.models import Exam
from apps.core.permissions import IsTeacher, IsAdmin


@extend_schema(tags=['Certificates'])
class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.filter(is_active=True)
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['super_admin', 'admin', 'teacher']:
            return Certificate.objects.filter(is_active=True)
        return Certificate.objects.filter(user=user, is_active=True)


@extend_schema(tags=['Certificates'])
class IssueCertificateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    @extend_schema(tags=['Certificates'], request=IssueCertificateSerializer)
    def post(self, request):
        serializer = IssueCertificateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data['user_id']
        course_id = serializer.validated_data.get('course_id')
        exam_id = serializer.validated_data.get('exam_id')
        title = serializer.validated_data.get('title', '')

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        course = Course.objects.filter(id=course_id).first() if course_id else None
        exam = Exam.objects.filter(id=exam_id).first() if exam_id else None

        if not title:
            title = course.title if course else (exam.title if exam else "EDUQASH Certificate")

        cert = Certificate.objects.create(
            user=user,
            course=course,
            exam=exam,
            title=title
        )

        CertificateGenerator.generate_pdf_and_qr(cert)

        return Response({
            'message': 'Certificate issued successfully.',
            'certificate': CertificateSerializer(cert).data
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Certificates'])
class VerifyCertificateView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(tags=['Certificates'])
    def get(self, request, unique_id):
        cert = Certificate.objects.filter(unique_id=unique_id, is_active=True).first()
        if not cert:
            return Response({
                'valid': False,
                'message': 'Certificate not found or invalid.'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'valid': True,
            'certificate': CertificateSerializer(cert).data
        }, status=status.HTTP_200_OK)
