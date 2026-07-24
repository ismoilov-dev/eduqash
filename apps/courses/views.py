from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.courses.models import Course, Lesson, Homework, HomeworkSubmission
from apps.courses.serializers import (
    CourseSerializer,
    LessonSerializer,
    HomeworkSerializer,
    HomeworkSubmissionSerializer,
)
from apps.core.permissions import IsTeacher, IsAdmin, IsOwnerOrReadOnly


@extend_schema_view(
    list=extend_schema(summary="Kurslar ro'yxatini ko'rish"),
    create=extend_schema(summary="Yangi kurs yaratish (O'qituvchi/Admin)"),
    retrieve=extend_schema(summary="Kurs ma'lumotlarini ko'rish"),
    update=extend_schema(summary="Kurs ma'lumotlarini to'liq tahrirlash"),
    partial_update=extend_schema(summary="Kurs ma'lumotlarini qisman tahrirlash"),
    destroy=extend_schema(summary="Kursni o'chirish"),
)
@extend_schema(tags=['Courses'])
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['type', 'teacher', 'center']
    ordering_fields = ['price', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.AllowAny()]


@extend_schema_view(
    list=extend_schema(summary="Darslar ro'yxatini ko'rish"),
    create=extend_schema(summary="Yangi dars qo'shish (O'qituvchi)"),
    retrieve=extend_schema(summary="Dars tafsilotlarini ko'rish"),
    update=extend_schema(summary="Darsni to'liq tahrirlash"),
    partial_update=extend_schema(summary="Darsni qisman tahrirlash"),
    destroy=extend_schema(summary="Darsni o'chirish"),
)
@extend_schema(tags=['Courses'])
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(is_active=True)
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']
    filterset_fields = ['course']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]


@extend_schema_view(
    list=extend_schema(summary="Uy vazifalari ro'yxatini ko'rish"),
    create=extend_schema(summary="Yangi uy vazifasi yaratish (O'qituvchi)"),
    retrieve=extend_schema(summary="Uy vazifasini ko'rish"),
    update=extend_schema(summary="Uy vazifasini to'liq tahrirlash"),
    partial_update=extend_schema(summary="Uy vazifasini qisman tahrirlash"),
    destroy=extend_schema(summary="Uy vazifasini o'chirish"),
)
@extend_schema(tags=['Courses'])
class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.filter(is_active=True)
    serializer_class = HomeworkSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['lesson']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]


@extend_schema_view(
    list=extend_schema(summary="Topshirilgan uy vazifalari ro'yxati"),
    create=extend_schema(summary="Uy vazifasini topshirish (Talaba)"),
    retrieve=extend_schema(summary="Topshirilgan uy vazifasi tafsilotlari"),
    update=extend_schema(summary="Uy vazifasini baholash va feedback berish (O'qituvchi)"),
    partial_update=extend_schema(summary="Uy vazifasini qisman baholash"),
    destroy=extend_schema(summary="Topshirilgan vazifani o'chirish"),
)
@extend_schema(tags=['Courses'])
class HomeworkSubmissionViewSet(viewsets.ModelViewSet):
    queryset = HomeworkSubmission.objects.filter(is_active=True)
    serializer_class = HomeworkSubmissionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['homework', 'student']

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['super_admin', 'admin', 'teacher']:
            return HomeworkSubmission.objects.filter(is_active=True)
        return HomeworkSubmission.objects.filter(student=user, is_active=True)
