from rest_framework.routers import DefaultRouter
from apps.exams.views import (
    ExamViewSet,
    ExamSectionViewSet,
    QuestionViewSet,
    ExamAttemptViewSet,
)

# Exams & Band Score Calculator API Endpoints (Frontend uchun)
# Base path: /exams/
router = DefaultRouter()

# 1. Imtihon bo'limlari (Exam Sections: Listening, Reading, Writing, Speaking)
# - GET /exams/sections/ : Bo'limlar ro'yxati (?exam=<exam_id>)
# - POST /exams/sections/ : Bo'lim qo'shish (Teacher/Admin)
# - GET/PUT/PATCH/DELETE /exams/sections/{id}/ : Bo'limni ko'rish/tahrirlash/o'chirish
router.register(r'sections', ExamSectionViewSet, basename='exam-sections')

# 2. Savollar (Questions)
# - GET /exams/questions/ : Savollar ro'yxati (?section=<section_id>&question_type=multiple_choice|text)
# - POST /exams/questions/ : Savol qo'shish (Teacher/Admin)
# - GET/PUT/PATCH/DELETE /exams/questions/{id}/ : Savolni ko'rish/tahrirlash/o'chirish
router.register(r'questions', QuestionViewSet, basename='exam-questions')

# 3. Urinishlar va topshirishlar (Exam Attempts)
# - GET /exams/attempts/ : Foydalanuvchining imtihon topshirganlik tarixi (Authed)
# - GET /exams/attempts/{id}/ : Imtihon urinishi tafsilotlari va to'plangan Band Score
# - POST /exams/attempts/{id}/submit/ : Imtihon javoblarini topshirish (Payload: {answers: [{question_id, selected_choice_id, text_answer}]}) -> Avtomatik baholaydi va IELTS band hisoblaydi
router.register(r'attempts', ExamAttemptViewSet, basename='exam-attempts')

# 4. Imtihonlar (Exams)
# - GET /exams/ : Imtihonlar ro'yxati (?exam_type=ielts_mock|cefr|custom&search=...)
# - POST /exams/ : Yangi imtihon yaratish (Teacher/Admin)
# - GET/PUT/PATCH/DELETE /exams/{id}/ : Imtihonni ko'rish/tahrirlash/o'chirish
# - POST /exams/{id}/start_attempt/ : Imtihonni topshirishni boshlash (Attempt obyekti yaratib beradi)
router.register(r'', ExamViewSet, basename='exams')

urlpatterns = router.urls
