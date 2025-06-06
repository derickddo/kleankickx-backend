from rest_framework import serializers
from .models import LoyaltyPoint

class LoyaltyPointSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id', read_only=True, allow_null=True)
    source_display = serializers.CharField(source='get_source_display', read_only=True)

    class Meta:
        model = LoyaltyPoint
        fields = ['id', 'points', 'source', 'source_display', 'order_id', 'created_at']