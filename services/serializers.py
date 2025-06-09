from rest_framework import serializers
from .models import Service
import base64

class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for the Service model, including image handling."""
    image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'price', 'created_at', 'updated_at', 'image'
        ]
    def get_image(self, obj):
        if obj.image:
            # Encode binary image as base64
            return f"data:image/jpeg;base64,{base64.b64encode(obj.image).decode('utf-8')}"
        return None


    def validate(self, data):
        if data.get('price') < 0:
            raise serializers.ValidationError("Price cannot be negative.")
       