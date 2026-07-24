from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.payments.views import (
    PaymentViewSet,
    PromoCodeViewSet,
    CreatePaymentView,
    VerifyPaymentView,
    ApplyPromoView,
)

# Payments & Promo Codes API Endpoints (Frontend uchun)
# Base path: /payments/
router = DefaultRouter()

# 1. Promokodlar boshqaruvi (Admin)
# - GET /payments/promos/ : Promokodlar ro'yxati
# - POST /payments/promos/ : Yangi promokod yaratish (Payload: {code, discount_percent, valid_until, usage_limit})
# - GET/PUT/PATCH/DELETE /payments/promos/{id}/ : Promokodni tahrirlash/o'chirish
router.register(r'promos', PromoCodeViewSet, basename='promo-codes')

# 2. To'lovlar tarixi (Payments History)
# - GET /payments/ : To'lovlar ro'yxati (Foydalanuvchi o'z to'lovlarini, Admin barcha to'lovlarni ko'radi)
# - GET /payments/{id}/ : To'lov tafsilotini ko'rish
router.register(r'', PaymentViewSet, basename='payments')

urlpatterns = [
    # 3. Yangi to'lov yaratish (POST, Authed) -> Payload: {course_id, amount, provider: "payme"|"click"|"fake", promo_code}
    path('create/', CreatePaymentView.as_view(), name='payments_create'),
    
    # 4. To'lovni tasdiqlash (POST, Authed) -> Payload: {transaction_id} -> Res: {payment, status: "paid"}
    path('verify/', VerifyPaymentView.as_view(), name='payments_verify'),
    
    # 5. Promokod qo'llash va tekshirish (POST, Authed) -> Payload: {code} -> Res: {discount_percent, message}
    path('apply-promo/', ApplyPromoView.as_view(), name='payments_apply_promo'),
] + router.urls
