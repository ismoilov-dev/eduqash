from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'role_approval_status', 'rejection_reason',
            'is_email_verified', 'phone', 'telegram_id', 
            'avatar', 'bio', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'is_email_verified', 'role_approval_status', 'rejection_reason', 'created_at', 'updated_at')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone', 'bio')

    def validate_role(self, value):
        allowed_roles = ('student', 'teacher', 'center_owner')
        if value not in allowed_roles:
            raise serializers.ValidationError("Ushbu rol bilan to'g'ridan-to me'yorida ro'yxatdan o'tib bo'lmaydi.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['role_approval_status'] = 'pending'

        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username yoki Email kiriting")
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_val = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username_val).first() or User.objects.filter(email=username_val).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "User account is disabled."})

        if user.role_approval_status == 'pending':
            raise serializers.ValidationError({
                "detail": "Sizning rolingiz hali admin tomonidan tasdiqlanmagan. Iltimos admin tasdiqlashini kuting."
            })

        if user.role_approval_status == 'rejected':
            reason = f" Sabab: {user.rejection_reason}" if user.rejection_reason else ""
            raise serializers.ValidationError({
                "detail": f"Sizning ariza rolingiz admin tomonidan rad etilgan.{reason}"
            })

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


class AdminApproveRoleSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    rejection_reason = serializers.CharField(required=False, allow_blank=True)

