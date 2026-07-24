from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.exams.models import Exam, ExamSection, Question, AnswerChoice, ExamAttempt, UserAnswer
from apps.exams.serializers import (
    ExamSerializer,
    ExamSectionSerializer,
    QuestionSerializer,
    AnswerChoiceSerializer,
    ExamAttemptSerializer,
    SubmitExamSerializer,
)
from apps.exams.band_calculator import BandCalculatorService
from apps.core.permissions import IsTeacher, IsAdmin


@extend_schema_view(
    list=extend_schema(summary="Imtihonlar ro'yxatini ko'rish"),
    create=extend_schema(summary="Yangi imtihon yaratish (O'qituvchi/Admin)"),
    retrieve=extend_schema(summary="Imtihon tafsilotlarini ko'rish"),
    update=extend_schema(summary="Imtihonni to'liq tahrirlash"),
    partial_update=extend_schema(summary="Imtihonni qisman tahrirlash"),
    destroy=extend_schema(summary="Imtihonni o'chirish"),
)
@extend_schema(tags=['Exams'])
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.filter(is_active=True)
    serializer_class = ExamSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['exam_type']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.AllowAny()]

    @extend_schema(summary="Imtihon topshirishni boshlash (Attempt yaratish)", request=None, responses={201: ExamAttemptSerializer})
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def start_attempt(self, request, pk=None):
        exam = self.get_object()
        attempt = ExamAttempt.objects.create(
            exam=exam,
            student=request.user
        )
        return Response(ExamAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    list=extend_schema(summary="Imtihon bo'limlari (Listening, Reading...) ro'yxati"),
    create=extend_schema(summary="Yangi bo'lim qo'shish (O'qituvchi)"),
    retrieve=extend_schema(summary="Imtihon bo'limi tafsilotlari"),
    update=extend_schema(summary="Imtihon bo'limini to'liq tahrirlash"),
    partial_update=extend_schema(summary="Imtihon bo'limini qisman tahrirlash"),
    destroy=extend_schema(summary="Imtihon bo'limini o'chirish"),
)
@extend_schema(tags=['Exams'])
class ExamSectionViewSet(viewsets.ModelViewSet):
    queryset = ExamSection.objects.filter(is_active=True)
    serializer_class = ExamSectionSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)
    filterset_fields = ['exam']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.AllowAny()]


@extend_schema_view(
    list=extend_schema(summary="Imtihon savollari ro'yxatini ko'rish"),
    create=extend_schema(summary="Yangi savol qo'shish (O'qituvchi)"),
    retrieve=extend_schema(summary="Savol tafsilotlarini ko'rish"),
    update=extend_schema(summary="Savolni to'liq tahrirlash"),
    partial_update=extend_schema(summary="Savolni qisman tahrirlash"),
    destroy=extend_schema(summary="Savolni o'chirish"),
)
@extend_schema(tags=['Exams'])
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True)
    serializer_class = QuestionSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)
    filterset_fields = ['section', 'question_type']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.AllowAny()]


@extend_schema_view(
    list=extend_schema(summary="Imtihon savollarining javob variantlari ro'yxati"),
    create=extend_schema(summary="Savolga yangi javob varianti qo'shish (O'qituvchi)"),
    retrieve=extend_schema(summary="Javob varianti tafsilotlari"),
    update=extend_schema(summary="Javob variantini to'liq tahrirlash"),
    partial_update=extend_schema(summary="Javob variantini qisman tahrirlash"),
    destroy=extend_schema(summary="Javob variantini o'chirish"),
)
@extend_schema(tags=['Exams'])
class AnswerChoiceViewSet(viewsets.ModelViewSet):
    queryset = AnswerChoice.objects.filter(is_active=True)
    serializer_class = AnswerChoiceSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)
    filterset_fields = ['question', 'is_correct']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.AllowAny()]


@extend_schema_view(
    list=extend_schema(summary="Foydalanuvchining topshirgan imtihonlari tarixi"),
    retrieve=extend_schema(summary="Imtihon topshirish natijasi va Band Score"),
)
@extend_schema(tags=['Exams'])
class ExamAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExamAttempt.objects.filter(is_active=True)
    serializer_class = ExamAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['super_admin', 'admin', 'teacher']:
            return ExamAttempt.objects.filter(is_active=True)
        return ExamAttempt.objects.filter(student=user, is_active=True)

    @extend_schema(summary="Imtihon javoblarini topshirish va IELTS Band Score hisoblash", request=SubmitExamSerializer)
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        if attempt.is_completed:
            return Response({'error': 'Exam attempt already submitted.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SubmitExamSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        answers_data = serializer.validated_data['answers']
        total_score = 0.0

        for ans in answers_data:
            q_id = ans['question_id']
            choice_id = ans.get('selected_choice_id')
            text_ans = ans.get('text_answer')

            question = Question.objects.filter(id=q_id).first()
            if not question:
                continue

            is_correct = False
            score_awarded = 0.0

            if choice_id:
                choice = AnswerChoice.objects.filter(id=choice_id, question=question).first()
                if choice and choice.is_correct:
                    is_correct = True
                    score_awarded = float(question.points)
            elif text_ans:
                correct_choice = AnswerChoice.objects.filter(question=question, is_correct=True).first()
                if correct_choice and correct_choice.text.strip().lower() == text_ans.strip().lower():
                    is_correct = True
                    score_awarded = float(question.points)

            total_score += score_awarded
            UserAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_choice_id=choice_id if choice_id else None,
                text_answer=text_ans,
                is_correct=is_correct,
                score_awarded=score_awarded
            )

        attempt.score = total_score
        attempt.end_time = timezone.now()
        attempt.is_completed = True
        attempt.band_score = BandCalculatorService.calculate_band(
            exam_type=attempt.exam.exam_type,
            raw_score=total_score,
            total_questions=attempt.exam.total_questions
        )
        attempt.save()

        return Response({
            'message': 'Exam submitted successfully.',
            'attempt': ExamAttemptSerializer(attempt).data
        }, status=status.HTTP_200_OK)
