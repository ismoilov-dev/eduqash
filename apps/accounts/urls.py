from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.accounts.views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    GoogleAuthView,
    TelegramAuthView,
    ForgotPasswordView,
    ResetPasswordView,
    ChangePasswordView,
    ProfileView,
)

# Accounts & Auth API Endpoints (Frontend uchun)
urlpatterns = [
    # 1. Ro'yxatdan o'tish (POST) -> Payload: {username, email, password, first_name, last_name, role}
    path('register/', RegisterView.as_view(), name='auth_register'),
    
    # 2. Tizimga kirish (POST) -> Payload: {email_or_username, password} -> Res: {user, tokens: {access, refresh}}
    path('login/', LoginView.as_view(), name='auth_login'),
    
    # 3. Email tasdiqlash (POST) -> Payload: {email, code} -> Res: {message}
    path('verify-email/', VerifyEmailView.as_view(), name='auth_verify_email'),
    
    # 4. Google bilan kirish/ro'yxatdan o'tish (POST) -> Payload: {email, google_id, first_name, last_name}
    path('google/', GoogleAuthView.as_view(), name='auth_google'),
    
    # 5. Telegram bilan kirish/ro'yxatdan o'tish (POST) -> Payload: {telegram_id, first_name, last_name, username}
    path('telegram/', TelegramAuthView.as_view(), name='auth_telegram'),
    
    # 6. JWT Tokenni yangilash (POST) -> Payload: {refresh} -> Res: {access}
    path('token/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),
    
    # 7. Parolni unutganda emailga kod yuborish (POST) -> Payload: {email}
    path('forgot-password/', ForgotPasswordView.as_view(), name='auth_forgot_password'),
    
    # 8. Email kodi orqali parolni yangilash (POST) -> Payload: {email, code, new_password}
    path('reset-password/', ResetPasswordView.as_view(), name='auth_reset_password'),
    
    # 9. Tizimdagi foydalanuvchi parolini o'zgartirishi (POST, Authed) -> Payload: {old_password, new_password}
    path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
    
    # 10. Profil ma'lumotlarini olish va tahrirlash (GET / PUT / PATCH, Authed) -> Header: Authorization: Bearer <access_token>
    path('profile/', ProfileView.as_view(), name='auth_profile'),
]
