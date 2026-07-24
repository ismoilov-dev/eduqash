from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from apps.exams.models import Exam, ExamSection, Question, AnswerChoice, ExamAttempt, UserAnswer


class AnswerChoiceInline(TabularInline):
    model = AnswerChoice
    extra = 2


class QuestionInline(TabularInline):
    model = Question
    extra = 1


class ExamSectionInline(TabularInline):
    model = ExamSection
    extra = 1


@admin.register(Exam)
class ExamAdmin(ModelAdmin):
    list_display = ('title', 'exam_type', 'duration_minutes', 'total_questions', 'passing_score', 'is_active', 'created_at')
    list_filter = ('exam_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    inlines = [ExamSectionInline]


@admin.register(ExamSection)
class ExamSectionAdmin(ModelAdmin):
    list_display = ('title', 'exam', 'order', 'created_at')
    list_filter = ('exam__exam_type', 'created_at')
    search_fields = ('title', 'passage_text')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ('text', 'section', 'question_type', 'points', 'order')
    list_filter = ('question_type', 'section__exam')
    search_fields = ('text',)
    inlines = [AnswerChoiceInline]


@admin.register(ExamAttempt)
class ExamAttemptAdmin(ModelAdmin):
    list_display = ('student', 'exam', 'score', 'band_score', 'is_completed', 'created_at')
    list_filter = ('exam__exam_type', 'is_completed', 'created_at')
    search_fields = ('student__username', 'exam__title', 'band_score')


@admin.register(UserAnswer)
class UserAnswerAdmin(ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct', 'score_awarded')
    list_filter = ('is_correct',)
