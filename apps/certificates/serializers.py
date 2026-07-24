from rest_framework import serializers
from apps.certificates.models import Certificate
from apps.accounts.serializers import UserSerializer
from apps.courses.serializers import CourseSerializer
from apps.exams.serializers import ExamSerializer


class CertificateSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    course_details = CourseSerializer(source='course', read_only=True)
    exam_details = ExamSerializer(source='exam', read_only=True)

    class Meta:
        model = Certificate
        fields = '__all__'
        read_only_fields = ('unique_id', 'qr_code', 'pdf_file', 'issue_date', 'created_at', 'updated_at')


class IssueCertificateSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    course_id = serializers.UUIDField(required=False, allow_null=True)
    exam_id = serializers.UUIDField(required=False, allow_null=True)
    title = serializers.CharField(required=False, allow_blank=True)
