from rest_framework import serializers
from apps.payments.models import Payment, PromoCode
from apps.accounts.serializers import UserSerializer
from apps.courses.serializers import CourseSerializer


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'


class CreatePaymentSerializer(serializers.Serializer):
    course_id = serializers.UUIDField(required=False, allow_null=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    provider = serializers.ChoiceField(choices=Payment.PROVIDER_CHOICES, default='fake')
    promo_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class VerifyPaymentSerializer(serializers.Serializer):
    transaction_id = serializers.CharField()


class ApplyPromoSerializer(serializers.Serializer):
    code = serializers.CharField()


class PaymentSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    course_details = CourseSerializer(source='course', read_only=True)
    promo_details = PromoCodeSerializer(source='promo_code', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', 'status', 'transaction_id', 'created_at', 'updated_at')
