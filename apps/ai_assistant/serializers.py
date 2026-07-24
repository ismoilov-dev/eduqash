from rest_framework import serializers


class EssayCheckSerializer(serializers.Serializer):
    essay_text = serializers.CharField(min_length=20)
    topic = serializers.CharField(required=False, allow_blank=True)


class GrammarFixSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=3)


class RoadmapSerializer(serializers.Serializer):
    target_goal = serializers.CharField()
    current_level = serializers.CharField()


class HomeworkCheckSerializer(serializers.Serializer):
    homework_description = serializers.CharField()
    submission_text = serializers.CharField()
