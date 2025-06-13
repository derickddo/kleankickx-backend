```python
# kleankickx-backend/delivery/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Delivery
from .serializers import DeliverySerializer
import requests
from django.conf import settings

YANGO_API_KEY = settings.YANGO_API_KEY

class DeliveryCostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            delivery_lat = request.data.get('delivery_latitude')
            delivery_lon = request.data.get('delivery_longitude')
            if not delivery_lat or not delivery_lon:
                return Response(
                    {'error': 'Delivery coordinates required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Hypothetical Yango API call
            response = requests.post(
                'https://api.yango.com/v1/estimate',
                json={
                    'pickup': {'lat': 5.6037, 'lon': -0.1870},  # KleanKickx warehouse
                    'delivery': {'lat': delivery_lat, 'lon': delivery_lon},
                },
                headers={'Authorization': f'Bearer {YANGO_API_KEY}'}
            )
            response.raise_for_status()
            data = response.json()
            cost = data.get('cost', 0)

            delivery_data = {
                'delivery_cost': cost,
                'status': 'PICKED_UP',
            }
            serializer = DeliverySerializer(data=delivery_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'delivery_cost': cost,
                        'delivery_id': serializer.data['id'],
                    },
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except requests.RequestException as e:
            return Response({'error': f'Yango API error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeliveryStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, delivery_id):
        try:
            delivery = Delivery.objects.get(id=delivery_id)
            serializer = DeliverySerializer(delivery)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Delivery.DoesNotExist:
            return Response({'error': 'Delivery not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)