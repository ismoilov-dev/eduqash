from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from apps.quizzes.models import (
    QuestionBank,
    QuizQuestion,
    QuizQuestionOption,
    Quiz,
    QuizAttempt,
    Leaderboard,
)


class QuizQuestionOptionInline(TabularInline):
    model = QuizQuestionOption
    extra = 2


@admin.register(QuestionBank)
class QuestionBankAdmin(ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    search_fields = ('title', 'description', 'owner__username')


@admin.register(QuizQuestion)
class QuizQuestionAdmin(ModelAdmin):
    list_display = ('text', 'bank', 'type', 'points', 'negative_marking')
    list_filter = ('type', 'bank')
    search_fields = ('text',)
    inlines = [QuizQuestionOptionInline]


@admin.register(Quiz)
class QuizAdmin(ModelAdmin):
    list_display = ('title', 'question_bank', 'timed', 'duration_minutes', 'created_at')
    list_filter = ('timed', 'created_at')
    search_fields = ('title', 'description')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'total_possible', 'completed_at')
    list_filter = ('quiz', 'completed_at')
    search_fields = ('student__username', 'quiz__title')


@admin.register(Leaderboard)
class LeaderboardAdmin(ModelAdmin):
    list_display = ('rank', 'student', 'quiz', 'score')
    list_filter = ('quiz',)
    ordering = ('rank',)
