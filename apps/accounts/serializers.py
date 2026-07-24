from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'is_email_verified', 'phone', 'telegram_id', 
            'avatar', 'bio', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'is_email_verified', 'created_at', 'updated_at')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        user = User.objects.filter(email=username_or_email).first() or User.objects.filter(username=username_or_email).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "User account is disabled."})

        attrs['user'] = user
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    google_id = serializers.CharField()


class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
