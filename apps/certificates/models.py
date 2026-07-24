import uuid
from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.courses.models import Course
from apps.exams.models import Exam


class Certificate(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='certificates'
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='certificates'
    )
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='certificates/qrcodes/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='certificates/pdfs/', blank=True, null=True)
    issue_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Certificate {self.unique_id} - {self.user.username}"
