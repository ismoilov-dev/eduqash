from rest_framework import serializers
from apps.centers.models import LearningCenter
from apps.accounts.serializers import UserSerializer


class LearningCenterSerializer(serializers.ModelSerializer):
    owner_details = UserSerializer(source='owner', read_only=True)

    class Meta:
        model = LearningCenter
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'rating', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
