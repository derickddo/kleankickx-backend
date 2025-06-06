# # addresses/views.py
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Address
# from .serializers import AddressSerializer
# from .utils import get_coordinates_from_address  # To be implemented
# from django.core.exceptions import ValidationError

# class AddressView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """List all addresses for the authenticated user."""
#         addresses = Address.objects.filter(user=request.user)
#         serializer = AddressSerializer(addresses, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         """Create a new address with optional map-based coordinates."""
#         data = request.data.copy()
#         # If map-based coordinates are not provided, attempt to geocode
#         if not (data.get('latitude') and data.get('longitude')):
#             latitude, longitude = get_coordinates_from_address(
#                 data.get('location', ''), data.get('region', '')
#             )
#             if latitude and longitude:
#                 data['latitude'] = latitude
#                 data['longitude'] = longitude

#         serializer = AddressSerializer(data=data, context={'request': request})
#         if serializer.is_valid():
#             address = serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AddressDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         """Retrieve a specific address."""
#         try:
#             address = Address.objects.get(pk=pk, user=request.user)
#             serializer = AddressSerializer(address)
#             return Response(serializer.data)
#         except Address.DoesNotExist:
#             return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, pk):
#         """Update an existing address."""
#         try:
#             address = Address.objects.get(pk=pk, user=request.user)
#             serializer = AddressSerializer(address, data=request.data, context={'request': request})
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Address.DoesNotExist:
#             return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, pk):
#         """Delete an address."""
#         try:
#             address = Address.objects.get(pk=pk, user=request.user)
#             address.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Address.DoesNotExist:
#             return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)