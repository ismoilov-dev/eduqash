from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class QuestionBank(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='question_banks'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class QuizQuestion(BaseModel):
    QUESTION_TYPE_CHOICES = (
        ('single', 'Single Choice'),
        ('multi', 'Multiple Choice'),
        ('text', 'Text Answer'),
    )

    bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='single')
    shuffle = models.BooleanField(default=True)
    negative_marking = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    points = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)

    def __str__(self):
        return self.text[:50]


class QuizQuestionOption(BaseModel):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"


class Quiz(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='quizzes')
    timed = models.BooleanField(default=True)
    duration_minutes = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class QuizAttempt(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    total_possible = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-completed_at']

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.score}/{self.total_possible})"


class Leaderboard(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='leaderboard')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6, decimal_places=2)
    rank = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['rank']
