from rest_framework import serializers
from .models import Payment
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['job']
    extra_kwargs = {
            'job': {'required': True},  # Make the 'job' field required
        }
