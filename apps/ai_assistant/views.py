from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema

from apps.ai_assistant.serializers import (
    EssayCheckSerializer,
    GrammarFixSerializer,
    RoadmapSerializer,
    HomeworkCheckSerializer,
)
from apps.ai_assistant.ai_service import AIService


@extend_schema(tags=['AI Assistant'])
class CheckEssayView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EssayCheckSerializer

    @extend_schema(summary="Inshoni AI bilan tahlil qilish va IELTS Band bashorat qilish", request=EssayCheckSerializer)
    def post(self, request):
        serializer = EssayCheckSerializer(data=request.data)
        if serializer.is_valid():
            essay_text = serializer.validated_data['essay_text']
            topic = serializer.validated_data.get('topic', '')
            feedback = AIService.check_essay(essay_text, prompt_topic=topic)
            band_prediction = AIService.writing_band_prediction(essay_text)
            return Response({
                'feedback': feedback,
                'band_prediction': band_prediction
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['AI Assistant'])
class GrammarFixView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GrammarFixSerializer

    @extend_schema(summary="Matndagi grammatik xatolarni AI orqali tuzatish", request=GrammarFixSerializer)
    def post(self, request):
        serializer = GrammarFixSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            correction = AIService.grammar_fix(text)
            return Response({'correction': correction}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['AI Assistant'])
class RoadmapView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoadmapSerializer

    @extend_schema(summary="Individual o'quv rejasini (Roadmap) AI yordamida generatsiya qilish", request=RoadmapSerializer)
    def post(self, request):
        serializer = RoadmapSerializer(data=request.data)
        if serializer.is_valid():
            target_goal = serializer.validated_data['target_goal']
            current_level = serializer.validated_data['current_level']
            roadmap = AIService.generate_roadmap(target_goal, current_level)
            return Response({'roadmap': roadmap}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['AI Assistant'])
class CheckHomeworkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HomeworkCheckSerializer

    @extend_schema(summary="Uy vazifasini AI bilan avtomatik tekshirish va baholash", request=HomeworkCheckSerializer)
    def post(self, request):
        serializer = HomeworkCheckSerializer(data=request.data)
        if serializer.is_valid():
            homework_description = serializer.validated_data['homework_description']
            submission_text = serializer.validated_data['submission_text']
            result = AIService.check_homework(homework_description, submission_text)
            return Response({'evaluation': result}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
