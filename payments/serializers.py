from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'method', 'amount', 'transaction_id', 'status']

    def validate(self, data):
        if data.get('amount', 0) <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        if not data.get('transaction_id'):
            raise serializers.ValidationError("Transaction ID required.")
        return data
