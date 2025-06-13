
from rest_framework import serializers
from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'status', 'delivery_cost']
        read_only_fields = ['id', 'status']
    def validate(self, data):
        if data.get('delivery_cost', 0) < 0:
            raise serializers.ValidationError("Delivery cost cannot be negative.")
        return data
