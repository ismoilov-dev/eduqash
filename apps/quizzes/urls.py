from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.quizzes.views import (
    QuestionBankViewSet,
    QuizViewSet,
    QuizAttemptViewSet,
    LeaderboardViewSet,
    ImportExcelView,
)

# Quizzes, Question Banks & Leaderboard API Endpoints (Frontend uchun)
# Base path: /quizzes/
router = DefaultRouter()

# 1. Savollar banki (Question Banks)
# - GET /quizzes/banks/ : Savol banklari ro'yxati (?search=...)
# - POST /quizzes/banks/ : Yangi bank yaratish (Teacher/Admin)
# - GET/PUT/PATCH/DELETE /quizzes/banks/{id}/ : Bankni boshqarish
router.register(r'banks', QuestionBankViewSet, basename='question-banks')

# 2. Quiz topshirishlar (Quiz Attempts)
# - GET /quizzes/attempts/ : Quiz topshirish tarixi (?quiz=...&student=...)
# - POST /quizzes/attempts/ : Quiz topshirish va natijani saqlash (Payload: {quiz, score, time_spent_seconds}) -> Avtomatik Leaderboard'ni yangilaydi
router.register(r'attempts', QuizAttemptViewSet, basename='quiz-attempts')

# 3. Peshqadamlar jadvali (Leaderboard)
# - GET /quizzes/leaderboard/ : Peshqadamlar reytingi (?quiz=<quiz_id>)
router.register(r'leaderboard', LeaderboardViewSet, basename='quiz-leaderboard')

# 4. Quizlar (Quizzes)
# - GET /quizzes/ : Quizlar ro'yxati (?question_bank=...&timed=true|false)
# - POST /quizzes/ : Yangi quiz yaratish (Teacher/Admin)
# - GET/PUT/PATCH/DELETE /quizzes/{id}/ : Quizni tahrirlash/o'chirish
router.register(r'', QuizViewSet, basename='quizzes')

urlpatterns = [
    # 5. Excel fayldan savollarni yuklash (POST, Teacher/Admin) -> Form-data: {file: <.xlsx>, bank_id: <bank_id>}
    path('import-excel/', ImportExcelView.as_view(), name='quizzes_import_excel'),
] + router.urls
