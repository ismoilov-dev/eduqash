from rest_framework import serializers
from apps.exams.models import Exam, ExamSection, Question, AnswerChoice, ExamAttempt, UserAnswer
from apps.accounts.serializers import UserSerializer


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    choices = AnswerChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'section', 'text', 'question_type', 'points', 'order', 'choices')


class ExamSectionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = ExamSection
        fields = ('id', 'exam', 'title', 'instructions', 'passage_text', 'audio_file', 'order', 'questions')


class ExamSerializer(serializers.ModelSerializer):
    sections = ExamSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'


class UserAnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    selected_choice_id = serializers.UUIDField(required=False, allow_null=True)
    text_answer = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class SubmitExamSerializer(serializers.Serializer):
    answers = UserAnswerSubmitSerializer(many=True)


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'


class ExamAttemptSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)
    user_answers = UserAnswerSerializer(many=True, read_only=True)
    exam_details = ExamSerializer(source='exam', read_only=True)

    class Meta:
        model = ExamAttempt
        fields = '__all__'
        read_only_fields = ('student', 'start_time', 'end_time', 'score', 'band_score', 'is_completed')
