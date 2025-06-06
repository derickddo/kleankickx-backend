from rest_framework import serializers
from .models import Address
from phonenumber_field.serializerfields import PhoneNumberField

class AddressSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = Address
        fields = [
            'id', 'name', 'phone_number', 'email', 'location', 'region',
            'landmark', 'latitude', 'longitude', 'is_default', 'created_at', 'updated_at'
        ]

    def validate(self, data):
        # Ensure latitude and longitude are provided together or not at all
        if (data.get('latitude') is not None and data.get('longitude') is None) or \
           (data.get('longitude') is not None and data.get('latitude') is None):
            raise serializers.ValidationError("Both latitude and longitude must be provided together.")
        return data

    def create(self, validated_data):
        # Ensure only one default address per user
        if validated_data.get('is_default'):
            Address.objects.filter(user=self.context['request'].user, is_default=True).update(is_default=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle default address logic
        if validated_data.get('is_default'):
            Address.objects.filter(user=instance.user, is_default=True).exclude(id=instance.id).update(is_default=False)
        return super().update(instance, validated_data)