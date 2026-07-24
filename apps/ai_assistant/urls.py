from django.urls import path
from apps.ai_assistant.views import (
    CheckEssayView,
    GrammarFixView,
    RoadmapView,
    CheckHomeworkView,
)

# AI Assistant Services API Endpoints (Frontend uchun)
# Base path: /ai/
urlpatterns = [
    # 1. Inshoni AI orqali tahlil qilish (POST, Authed) -> Payload: {essay_text, topic} -> Res: {feedback, band_prediction}
    path('check-essay/', CheckEssayView.as_view(), name='ai_check_essay'),
    
    # 2. Grammatik xatolarni tuzatish (POST, Authed) -> Payload: {text} -> Res: {correction}
    path('grammar-fix/', GrammarFixView.as_view(), name='ai_grammar_fix'),
    
    # 3. Individual o'quv rejasini (Roadmap) generatsiya qilish (POST, Authed) -> Payload: {target_goal, current_level} -> Res: {roadmap}
    path('roadmap/', RoadmapView.as_view(), name='ai_roadmap'),
    
    # 4. Uy vazifasini AI bilan tekshirish (POST, Authed) -> Payload: {homework_description, submission_text} -> Res: {evaluation}
    path('check-homework/', CheckHomeworkView.as_view(), name='ai_check_homework'),
]
