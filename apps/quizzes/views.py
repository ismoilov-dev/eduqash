from rest_framework import viewsets, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from apps.quizzes.models import QuestionBank, QuizQuestion, Quiz, QuizAttempt, Leaderboard
from apps.quizzes.serializers import (
    QuestionBankSerializer,
    QuizQuestionSerializer,
    QuizSerializer,
    QuizAttemptSerializer,
    LeaderboardSerializer,
    ExcelImportSerializer,
)
from apps.quizzes.excel_service import ExcelQuizImporter
from apps.core.permissions import IsTeacher, IsAdmin, IsOwnerOrReadOnly


@extend_schema(tags=['Quizzes'])
class QuestionBankViewSet(viewsets.ModelViewSet):
    queryset = QuestionBank.objects.filter(is_active=True)
    serializer_class = QuestionBankSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.AllowAny()]


@extend_schema(tags=['Quizzes'])
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['question_bank', 'timed']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.AllowAny()]


@extend_schema(tags=['Quizzes'])
class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.filter(is_active=True)
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['quiz', 'student']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['super_admin', 'admin', 'teacher']:
            return QuizAttempt.objects.filter(is_active=True)
        return QuizAttempt.objects.filter(student=user, is_active=True)

    def perform_create(self, serializer):
        attempt = serializer.save(student=self.request.user)

        # Update Leaderboard
        quiz = attempt.quiz
        attempts = QuizAttempt.objects.filter(quiz=quiz).order_by('-score', 'completed_at')
        Leaderboard.objects.filter(quiz=quiz).delete()

        rank = 1
        for att in attempts:
            Leaderboard.objects.create(
                quiz=quiz,
                student=att.student,
                score=att.score,
                rank=rank
            )
            rank += 1


@extend_schema(tags=['Quizzes'])
class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filterset_fields = ['quiz']


@extend_schema(tags=['Quizzes'])
class ImportExcelView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    @extend_schema(tags=['Quizzes'], request=ExcelImportSerializer)
    def post(self, request):
        serializer = ExcelImportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file_obj = serializer.validated_data['file']
        bank_id = serializer.validated_data['bank_id']

        bank = QuestionBank.objects.filter(id=bank_id).first()
        if not bank:
            return Response({'error': 'QuestionBank not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            imported_count = ExcelQuizImporter.import_from_excel(file_obj, bank)
            return Response({
                'message': f'Successfully imported {imported_count} questions from Excel.',
                'imported_count': imported_count
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Failed to parse Excel file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
