from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.centers.models import LearningCenter


class Course(BaseModel):
    COURSE_TYPE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    )

    type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='online')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    duration = models.CharField(max_length=100, help_text="e.g. 3 months / 60 hours")
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='taught_courses'
    )
    center = models.ForeignKey(
        LearningCenter,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='courses'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='courses/videos/', blank=True, null=True)
    pdf = models.FileField(upload_to='courses/pdfs/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Homework(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='homeworks/files/', blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class HomeworkSubmission(BaseModel):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='homework_submissions'
    )
    file = models.FileField(upload_to='homeworks/submissions/', blank=True, null=True)
    submission_text = models.TextField(blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"
