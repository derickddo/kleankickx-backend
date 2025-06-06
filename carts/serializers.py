# from rest_framework import serializers
# from services.models import Service
# from carts.models import Cart, CartItem
# from services.serializers import ServiceSerializer

# class CartItemSerializer(serializers.ModelSerializer):
#     service = ServiceSerializer(read_only=True)
#     service_id = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(), source='service', write_only=True
#     )

#     class Meta:
#         model = CartItem
#         fields = ['id', 'service', 'service_id', 'quantity']

# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True)
#     total_price = serializers.SerializerMethodField()

#     class Meta:
#         model = Cart
#         fields = ['id', 'items', 'total_price', 'created_at', 'updated_at']

#     def get_total_price(self, obj):
#         return sum(item.service.price * item.quantity for item in obj.items.all())