from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class Exam(BaseModel):
    EXAM_TYPE_CHOICES = (
        ('ielts_listening', 'IELTS Listening'),
        ('ielts_reading', 'IELTS Reading'),
        ('ielts_writing', 'IELTS Writing'),
        ('ielts_speaking', 'IELTS Speaking'),
        ('sat_math', 'SAT Math'),
        ('sat_reading', 'SAT Reading & Writing'),
        ('cefr_a1', 'CEFR A1'),
        ('cefr_a2', 'CEFR A2'),
        ('cefr_b1', 'CEFR B1'),
        ('cefr_b2', 'CEFR B2'),
        ('cefr_c1', 'CEFR C1'),
        ('cefr_c2', 'CEFR C2'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES)
    duration_minutes = models.PositiveIntegerField(default=60)
    total_questions = models.PositiveIntegerField(default=40)
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_exam_type_display()} - {self.title}"


class ExamSection(BaseModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    instructions = models.TextField(blank=True, null=True)
    passage_text = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='exams/audio/', max_length=500, blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.exam.title} - {self.title}"


class Question(BaseModel):
    QUESTION_TYPE_CHOICES = (
        ('single', 'Single Choice'),
        ('multi', 'Multiple Choice'),
        ('text', 'Text Input'),
    )

    section = models.ForeignKey(ExamSection, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='single')
    points = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Q: {self.text[:50]}"


class AnswerChoice(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"


class ExamAttempt(BaseModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exam_attempts'
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    band_score = models.CharField(max_length=50, blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.exam.title} ({self.band_score})"


class UserAnswer(BaseModel):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(AnswerChoice, on_delete=models.SET_NULL, blank=True, null=True)
    text_answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    score_awarded = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
