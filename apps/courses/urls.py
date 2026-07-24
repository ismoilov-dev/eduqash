from rest_framework.routers import DefaultRouter
from apps.courses.views import (
    CourseViewSet,
    LessonViewSet,
    HomeworkViewSet,
    HomeworkSubmissionViewSet,
)

# Courses, Lessons & Homeworks API Endpoints (Frontend uchun)
# Base path: /courses/
router = DefaultRouter()

# 1. Darslar (Lessons)
# - GET /courses/lessons/ : Darslar ro'yxati (?course=<course_id>&search=...)
# - POST /courses/lessons/ : Yangi dars qo'shish (Teacher/Admin)
# - GET/PUT/PATCH/DELETE /courses/lessons/{id}/ : Darsni ko'rish, tahrirlash yoki o'chirish
router.register(r'lessons', LessonViewSet, basename='lessons')

# 2. Uy vazifalari (Homeworks)
# - GET /courses/homeworks/ : Uy vazifalari ro'yxati (?lesson=<lesson_id>&search=...)
# - POST /courses/homeworks/ : Yangi uy vazifasi yaratish (Teacher/Admin)
# - GET/PUT/PATCH/DELETE /courses/homeworks/{id}/ : Uy vazifasini tahrirlash/o'chirish
router.register(r'homeworks', HomeworkViewSet, basename='homeworks')

# 3. Topshirilgan uy vazifalari (Homework Submissions)
# - GET /courses/submissions/ : Topshirilgan vazifalar ro'yxati (Student o'zinikini, Teacher hammanikini ko'radi)
# - POST /courses/submissions/ : Vazifani topshirish (Payload: {homework, submission_text, file})
# - GET/PUT/PATCH/DELETE /courses/submissions/{id}/ : Vazifani tekshirish va baholash (Teacher score/feedback yozadi)
router.register(r'submissions', HomeworkSubmissionViewSet, basename='homework-submissions')

# 4. Kurslar (Courses)
# - GET /courses/ : Kurslar ro'yxati (Params: ?type=online|offline&teacher=...&center=...&search=...&ordering=price)
# - POST /courses/ : Yangi kurs yaratish (Teacher/Admin)
# - GET/PUT/PATCH/DELETE /courses/{id}/ : Kursni ko'rish, tahrirlash va o'chirish
router.register(r'', CourseViewSet, basename='courses')

urlpatterns = router.urls
