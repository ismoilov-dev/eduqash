from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.payments.models import Payment, PromoCode
from apps.payments.serializers import (
    PaymentSerializer,
    PromoCodeSerializer,
    CreatePaymentSerializer,
    VerifyPaymentSerializer,
    ApplyPromoSerializer,
)
from apps.courses.models import Course
from apps.core.permissions import IsAdmin


@extend_schema_view(
    list=extend_schema(summary="To'lovlar tarixini ko'rish (User o'zinikini, Admin barchasini)"),
    retrieve=extend_schema(summary="To'lov kvitansiyasi tafsilotlarini ko'rish"),
)
@extend_schema(tags=['Payments'])
class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['super_admin', 'admin']:
            return Payment.objects.filter(is_active=True)
        return Payment.objects.filter(user=user, is_active=True)


@extend_schema(tags=['Payments'])
class CreatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreatePaymentSerializer

    @extend_schema(summary="Yangi to'lov yaratish (Payme, Click yoki Fake provider)", request=CreatePaymentSerializer, responses={201: PaymentSerializer})
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        course_id = serializer.validated_data.get('course_id')
        amount = serializer.validated_data['amount']
        provider = serializer.validated_data.get('provider', 'fake')
        promo_str = serializer.validated_data.get('promo_code')

        course = Course.objects.filter(id=course_id).first() if course_id else None
        promo = PromoCode.objects.filter(code=promo_str).first() if promo_str else None

        if promo and promo.discount_percent:
            amount = amount * (1 - (promo.discount_percent / 100))

        # Check FAKE_PAYMENT setting
        is_fake = getattr(settings, 'FAKE_PAYMENT', True) or provider == 'fake'
        payment_status = 'paid' if is_fake else 'pending'

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=amount,
            provider=provider,
            status=payment_status,
            promo_code=promo
        )

        if promo and payment_status == 'paid':
            promo.times_used += 1
            promo.save()

        return Response({
            'message': 'Payment created successfully.',
            'is_paid_instantly': payment_status == 'paid',
            'payment': PaymentSerializer(payment).data
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Payments'])
class VerifyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VerifyPaymentSerializer

    @extend_schema(summary="To'lov holatini tranzaksiya ID orqali tasdiqlash", request=VerifyPaymentSerializer, responses={200: PaymentSerializer})
    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tx_id = serializer.validated_data['transaction_id']
        payment = Payment.objects.filter(transaction_id=tx_id).first()
        if not payment:
            return Response({'error': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

        payment.status = 'paid'
        payment.save()
        return Response({
            'message': 'Payment verified and marked as paid.',
            'payment': PaymentSerializer(payment).data
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Payments'])
class ApplyPromoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplyPromoSerializer

    @extend_schema(summary="Promokodni tekshirish va chegirma foizini olish", request=ApplyPromoSerializer)
    def post(self, request):
        serializer = ApplyPromoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data['code']
        promo = PromoCode.objects.filter(code=code, is_active=True).first()

        if not promo:
            return Response({'error': 'Invalid or expired promo code.'}, status=status.HTTP_400_BAD_REQUEST)

        if promo.valid_until and promo.valid_until < timezone.now():
            return Response({'error': 'Promo code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        if promo.times_used >= promo.usage_limit:
            return Response({'error': 'Promo code usage limit reached.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'code': promo.code,
            'discount_percent': promo.discount_percent,
            'message': f'Promo code applied! {promo.discount_percent}% off.'
        }, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(summary="Promokodlar ro'yxatini ko'rish (Admin)"),
    create=extend_schema(summary="Yangi promokod yaratish (Admin)"),
    retrieve=extend_schema(summary="Promokod tafsilotlarini ko'rish"),
    update=extend_schema(summary="Promokodni to'liq tahrirlash"),
    partial_update=extend_schema(summary="Promokodni qisman tahrirlash"),
    destroy=extend_schema(summary="Promokodni o'chirish"),
)
@extend_schema(tags=['Payments'])
class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.filter(is_active=True)
    serializer_class = PromoCodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
