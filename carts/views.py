# from django.conf import settings
# from django.db import models
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import serializers
# from carts.models import Cart
# from carts.serializers import CartSerializer, CartItemSerializer


# class CartView(APIView):
#     def get(self, request):
#         user = request.user if request.user.is_authenticated else None
#         session_id = request.session.session_key if not user else None
#         cart, created = Cart.objects.get_or_create(user=user, session_id=session_id)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)

#     def post(self, request):
#         user = request.user if request.user.is_authenticated else None
#         session_id = request.session.session_key if not user else None
#         cart, created = Cart.objects.get_or_create(user=user, session_id=session_id)
#         serializer = CartItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(cart=cart)
#             return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)