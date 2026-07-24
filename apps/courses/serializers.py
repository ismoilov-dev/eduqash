from rest_framework import serializers
from apps.courses.models import Course, Lesson, Homework, HomeworkSubmission
from apps.accounts.serializers import UserSerializer
from apps.centers.serializers import LearningCenterSerializer


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)

    class Meta:
        model = HomeworkSubmission
        fields = '__all__'
        read_only_fields = ('id', 'student', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)


class HomeworkSerializer(serializers.ModelSerializer):
    submissions = HomeworkSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class LessonSerializer(serializers.ModelSerializer):
    homeworks = HomeworkSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class CourseSerializer(serializers.ModelSerializer):
    teacher_details = UserSerializer(source='teacher', read_only=True)
    center_details = LearningCenterSerializer(source='center', read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('id', 'teacher', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)
