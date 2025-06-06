from rest_framework import serializers
from .models import Service
from phonenumber_field.serializerfields import PhoneNumberField

class ServiceSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=False, allow_null=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'price', 'duration', 'category',
            'phone_number', 'created_at', 'updated_at'
        ]

    def validate(self, data):
        if data.get('price') < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        if data.get('duration') <= 0:
            raise serializers.ValidationError("Duration must be a positive number.")
        return data