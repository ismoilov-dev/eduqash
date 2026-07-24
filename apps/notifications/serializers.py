from rest_framework import serializers
from apps.notifications.models import Notification
from apps.accounts.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'user': {'required': False}
        }

    def create(self, validated_data):
        if 'user' not in validated_data and 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
