```python
# kleankickx-backend/payments/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
import requests
from django.conf import settings

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY

class PaymentInitializeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            amount = request.data.get('amount', 0)
            if amount <= 0:
                return Response({'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)

            # Convert to pesewas (Paystack expects kobo/pesewas)
            response = requests.post(
                'https://api.paystack.co/transaction/initialize',
                json={
                    'email': request.user.email,
                    'amount': int(amount * 100),  # e.g., GHS 57.75 -> 5775 pesewas
                    'currency': 'KES',
                    'callback_url': 'http://localhost:3000/checkout',  # Redirect after payment
                },
                headers={'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'}
            )
            response.raise_for_status()
            data = response.json()
            if not data.get('status'):
                return Response({'error': data.get('message')}, status=status.HTTP_400_BAD_REQUEST)

            payment_data = {
                'user': request.user,
                'method': 'PAYSTACK',
                'amount': amount,
                'transaction_id': data['data']['reference'],
                'status': 'PENDING',
            }
            serializer = PaymentSerializer(data=payment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'authorization_url': data['data']['authorization_url'],
                        'reference': data['data']['reference'],
                        'payment_id': serializer.data['id'],
                    },
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except requests.RequestException as e:
            return Response({'error': f'Paystack API error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            payment_id = request.data.get('payment_id')
            payment = Payment.objects.get(id=payment_id, user=request.user)
            if payment.status == 'SUCCESS':
                return Response({'status': 'SUCCESS'}, status=status.HTTP_200_OK)

            response = requests.get(
                f'https://api.paystack.co/transaction/verify/{payment.transaction_id}',
                headers={'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'}
            )
            response.raise_for_status()
            data = response.json()
            if data['status'] and data['data']['status'] == 'success':
                payment.status = 'SUCCESS'
                payment.save()
                return Response({'status': 'SUCCESS'}, status=status.HTTP_200_OK)
            return Response({'error': 'Payment not successful.'}, status=status.HTTP_400_BAD_REQUEST)

        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)
        except requests.RequestException as e:
            return Response({'error': f'Paystack API error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class PaymentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)