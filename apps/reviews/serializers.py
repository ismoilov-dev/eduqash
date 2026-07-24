from rest_framework import serializers
from apps.reviews.models import Review, ReviewReport
from apps.accounts.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'likes_count', 'dislikes_count', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReviewReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReport
        fields = '__all__'
        read_only_fields = ('reported_by', 'is_resolved', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['reported_by'] = self.context['request'].user
        return super().create(validated_data)
