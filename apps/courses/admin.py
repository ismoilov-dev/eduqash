from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from apps.courses.models import Course, Lesson, Homework, HomeworkSubmission


class LessonInline(TabularInline):
    model = Lesson
    extra = 1


class HomeworkInline(TabularInline):
    model = Homework
    extra = 1


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ('id', 'title', 'type', 'price', 'duration', 'teacher', 'center', 'is_active', 'created_at')
    list_filter = ('type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ('id', 'title', 'course', 'order', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'course__title')
    ordering = ('order', 'created_at')
    inlines = [HomeworkInline]


@admin.register(Homework)
class HomeworkAdmin(ModelAdmin):
    list_display = ('title', 'lesson', 'deadline', 'created_at')
    list_filter = ('lesson__course', 'deadline', 'created_at')
    search_fields = ('title', 'description')


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(ModelAdmin):
    list_display = ('homework', 'student', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('student__username', 'homework__title', 'feedback')
