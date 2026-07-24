import random
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.core.mail import send_mail
from django.conf import settings

from apps.accounts.models import User
from apps.accounts.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    VerifyEmailSerializer,
    GoogleAuthSerializer,
    TelegramAuthSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    AdminApproveRoleSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@extend_schema(tags=['Accounts'])
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(summary="Yangi foydalanuvchini ro'yxatdan o'tkazish", request=RegisterSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response({
                'user': UserSerializer(user).data,
                'tokens': None,
                'message': 'Ro\'yxatdan o\'tish arizangiz qabul qilindi. Admin tasdiqlaganidan so\'ng username yoki email va parolingiz orqali tizimga kira olasiz.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(summary="Tizimga kirish (Login)", request=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyEmailSerializer

    @extend_schema(summary="Email tasdiqlash kodi", request=VerifyEmailSerializer)
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            user = User.objects.filter(email=email, email_verification_code=code).first()

            if user:
                user.is_email_verified = True
                user.email_verification_code = None
                user.save()
                if user.role_approval_status == 'pending':
                    return Response({
                        'message': 'Email tasdiqlandi. Rolingiz admin tomonidan tasdiqlanishi kutilmoqda. Admin tasdiqlagach tizimga kirishingiz mumkin.'
                    }, status=status.HTTP_200_OK)

                return Response({'message': 'Email successfully verified.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid verification code or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class GoogleAuthView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAuthSerializer

    @extend_schema(summary="Google orqali avtorizatsiya", request=GoogleAuthSerializer)
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            google_id = serializer.validated_data['google_id']
            first_name = serializer.validated_data.get('first_name', '')
            last_name = serializer.validated_data.get('last_name', '')

            user = User.objects.filter(google_id=google_id).first() or User.objects.filter(email=email).first()

            if not user:
                username = email.split('@')[0] + "_" + str(random.randint(100, 999))
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    google_id=google_id,
                    is_email_verified=True,
                    role_approval_status='approved'
                )
            else:
                if not user.google_id:
                    user.google_id = google_id
                    user.is_email_verified = True
                    user.save()

            if user.role_approval_status == 'pending':
                return Response({'error': 'Sizning rolingiz admin tasdiqlashini kutilmoqda.'}, status=status.HTTP_403_FORBIDDEN)
            if user.role_approval_status == 'rejected':
                return Response({'error': f'Sizning ariza rolingiz rad etilgan. Sabab: {user.rejection_reason or ""}'}, status=status.HTTP_403_FORBIDDEN)

            tokens = get_tokens_for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class TelegramAuthView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TelegramAuthSerializer

    @extend_schema(summary="Telegram orqali avtorizatsiya", request=TelegramAuthSerializer)
    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        if serializer.is_valid():
            telegram_id = serializer.validated_data['telegram_id']
            first_name = serializer.validated_data.get('first_name', '')
            last_name = serializer.validated_data.get('last_name', '')
            username = serializer.validated_data.get('username', '') or f"tg_user_{telegram_id}"

            user = User.objects.filter(telegram_id=telegram_id).first()

            if not user:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    telegram_id=telegram_id,
                    is_email_verified=True,
                    role_approval_status='approved'
                )

            if user.role_approval_status == 'pending':
                return Response({'error': 'Sizning rolingiz admin tasdiqlashini kutilmoqda.'}, status=status.HTTP_403_FORBIDDEN)
            if user.role_approval_status == 'rejected':
                return Response({'error': f'Sizning ariza rolingiz rad etilgan. Sabab: {user.rejection_reason or ""}'}, status=status.HTTP_403_FORBIDDEN)

            tokens = get_tokens_for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordSerializer

    @extend_schema(summary="Parolni unutganda emailga tiklash kodini yuborish", request=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                code = str(random.randint(100000, 999999))
                user.password_reset_code = code
                user.save()
                try:
                    send_mail(
                        subject="EDUQASH PRO - Password Reset Code",
                        message=f"Your password reset code is: {code}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=True
                    )
                except Exception:
                    pass
            return Response({'message': 'If email is registered, password reset code has been sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    @extend_schema(summary="Email kodi orqali parolni yangilash", request=ResetPasswordSerializer)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']

            user = User.objects.filter(email=email, password_reset_code=code).first()
            if user:
                user.set_password(new_password)
                user.password_reset_code = None
                user.save()
                return Response({'message': 'Password reset successful. You can now login.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid code or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @extend_schema(summary="Parolni o'zgartirish (Avtorizatsiyadan o'tgan foydalanuvchi)", request=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Old password incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@extend_schema(tags=['Accounts'])
class AdminPendingRolesView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    @extend_schema(summary="Tasdiqlanishi kutilayotgan foydalanuvchilar ro'yxati (Admin)")
    def get_queryset(self):
        return User.objects.filter(role_approval_status='pending').order_by('-created_at')


@extend_schema(tags=['Accounts'])
class AdminApproveRoleView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminApproveRoleSerializer

    @extend_schema(summary="Foydalanuvchi rolini tasdiqlash yoki rad etish (Admin)", request=AdminApproveRoleSerializer)
    def post(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'error': 'Foydalanuvchi topilmadi.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminApproveRoleSerializer(data=request.data)
        if serializer.is_valid():
            action = serializer.validated_data['action']
            rejection_reason = serializer.validated_data.get('rejection_reason', '')

            if action == 'approve':
                user.role_approval_status = 'approved'
                user.rejection_reason = None
                user.save()
                return Response({
                    'message': f"Foydalanuvchi ({user.username}) roli ({user.role}) muvaffaqiyatli tasdiqlandi.",
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            elif action == 'reject':
                user.role_approval_status = 'rejected'
                user.rejection_reason = rejection_reason
                user.save()
                return Response({
                    'message': f"Foydalanuvchi ({user.username}) roli tasdiqlanmadi (Rad etildi).",
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

