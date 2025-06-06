# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Order, OrderItem
# from .serializers import OrderSerializer
# from cart.models import Cart, CartItem
# from delivery.utils import calculate_delivery_cost
# from addresses.models import Address
# from addresses.utils import get_coordinates_from_address
# from .tasks import send_order_confirmation
# from decimal import Decimal

# class OrderView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         cart = Cart.objects.filter(user=user).first()
#         if not cart or not cart.items.exists():
#             return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

#         # Get address
#         address_id = request.data.get('address_id')
#         delivery_data = request.data.get('delivery_data')
#         if address_id:
#             try:
#                 address = Address.objects.get(id=address_id, user=user)
#                 delivery_name = address.name
#                 delivery_phone = address.phone_number
#                 delivery_email = address.email
#                 delivery_address = address.location
#                 delivery_region = address.region
#                 delivery_landmark = address.landmark
#                 latitude = address.latitude
#                 longitude = address.longitude
#             except Address.DoesNotExist:
#                 return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
#         elif delivery_data:
#             delivery_name = delivery_data.get('name', user.username)
#             delivery_phone = delivery_data.get('phone_number', str(user.phone_number))
#             delivery_email = delivery_data.get('email', user.email)
#             delivery_address = delivery_data.get('address')
#             delivery_region = delivery_data.get('region')
#             delivery_landmark = delivery_data.get('landmark', '')
#             latitude = delivery_data.get('latitude')
#             longitude = delivery_data.get('longitude')
#             if not all([delivery_name, delivery_phone, delivery_email, delivery_address, delivery_region]):
#                 return Response({'error': 'Incomplete delivery details'}, status=status.HTTP_400_BAD_REQUEST)
#             if not (latitude and longitude):
#                 latitude, longitude = get_coordinates_from_address(delivery_address, delivery_region)
#             if delivery_data.get('save_address', False):
#                 Address.objects.create(
#                     user=user,
#                     name=delivery_name,
#                     phone_number=delivery_phone,
#                     email=delivery_email,
#                     location=delivery_address,
#                     region=delivery_region,
#                     landmark=delivery_landmark,
#                     latitude=latitude,
#                     longitude=longitude,
#                     is_default=delivery_data.get('is_default', False)
#                 )
#         else:
#             return Response({'error': 'Address or delivery details required'}, status=status.HTTP_400_BAD_REQUEST)

#         # Calculate delivery cost
#         if latitude and longitude:
#             try:
#                 delivery_cost = calculate_delivery_cost(latitude, longitude)
#             except Exception as e:
#                 return Response({'error': f'Delivery cost calculation failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             delivery_cost = 0

#         # Calculate total price and apply signup discount
#         total_price = sum(item.service.price * item.quantity for item in cart.items.all())
#         discount = Decimal('0.00')
#         if not user.signup_discount_used and request.data.get('apply_signup_discount', False):
#             discount = total_price * Decimal('0.10')  # 10% discount
#             total_price -= discount
#             user.signup_discount_used = True
#             user.save()

#         # Create order
#         order = Order.objects.create(
#             user=user,
#             total_price=total_price,
#             delivery_cost=delivery_cost,
#             discount=discount,  # Store discount amount
#             delivery_name=delivery_name,
#             delivery_phone=delivery_phone,
#             delivery_email=delivery_email,
#             delivery_address=delivery_address,
#             delivery_region=delivery_region,
#             delivery_landmark=delivery_landmark,
#             delivery_latitude=latitude,
#             delivery_longitude=longitude,
#         )

#         # Create order items
#         for item in cart.items.all():
#             OrderItem.objects.create(
#                 order=order,
#                 service=item.service,
#                 quantity=item.quantity,
#                 price=item.service.price
#             )

#         # Clear cart
#         cart.items.all().delete()

#         # Send confirmation
#         send_order_confirmation.delay(order.id)

#         return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)