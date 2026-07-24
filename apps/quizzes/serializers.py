from rest_framework import serializers
from apps.quizzes.models import (
    QuestionBank,
    QuizQuestion,
    QuizQuestionOption,
    Quiz,
    QuizAttempt,
    Leaderboard,
)
from apps.accounts.serializers import UserSerializer


class QuizQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestionOption
        fields = ('id', 'text', 'is_correct')


class QuizQuestionSerializer(serializers.ModelSerializer):
    options = QuizQuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ('id', 'bank', 'text', 'type', 'shuffle', 'negative_marking', 'points', 'options')


class QuestionBankSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionBank
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class QuizSerializer(serializers.ModelSerializer):
    bank_details = QuestionBankSerializer(source='question_bank', read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'


class QuizAttemptSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)

    class Meta:
        model = QuizAttempt
        fields = '__all__'
        read_only_fields = ('student', 'score', 'total_possible', 'completed_at')


class LeaderboardSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)

    class Meta:
        model = Leaderboard
        fields = '__all__'


class ExcelImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    bank_id = serializers.UUIDField()
