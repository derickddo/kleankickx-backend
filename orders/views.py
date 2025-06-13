from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from addresses.models import Address
from payments.models import Payment
from delivery.models import Delivery

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = request.data.get('cart', [])
            address_id = request.data.get('address_id')
            payment_id = request.data.get('payment_id')
            delivery_id = request.data.get('delivery_id')
            if not cart or not address_id or not payment_id or not delivery_id:
                return Response(
                    {'error': 'Cart, address, payment, and delivery details required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify references
            address = Address.objects.get(id=address_id, user=request.user)
            payment = Payment.objects.get(id=payment_id, user=request.user)
            delivery = Delivery.objects.get(id=delivery_id)

            if payment.status != 'SUCCESS':
                return Response(
                    {'error': 'Payment not confirmed.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Calculate totals
            subtotal = sum(item['quantity'] * item['price'] for item in cart)
            delivery_cost = delivery.delivery_cost
            tax_rate = 0.05  # 5% tax
            tax_amount = (subtotal + delivery_cost) * tax_rate
            total_amount = subtotal + delivery_cost + tax_amount

            # Prepare order data
            order_data = {
                'user': request.user,
                'address': address,
                'payment': payment,
                'delivery': delivery,
                'total_amount': total_amount,
                'subtotal': subtotal,
                'tax_amount': tax_amount,
                'items': [
                    {
                        'service_id': item['service_id'],
                        'quantity': item['quantity'],
                        'price': item['price'],
                    }
                    for item in cart
                ],
            }

            serializer = OrderSerializer(data=order_data)
            if serializer.is_valid():
                serializer.save()
                request.user.cart_data = []
                request.user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (Address.DoesNotExist, Payment.DoesNotExist, Delivery.DoesNotExist):
            return Response({'error': 'Invalid reference ID.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
