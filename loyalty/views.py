# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import LoyaltyPoint
# from .serializers import LoyaltyPointSerializer

# class LoyaltyPointView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """Retrieve loyalty points history and total for the user."""
#         points = LoyaltyPoint.objects.filter(user=request.user).order_by('-created_at')
#         serializer = LoyaltyPointSerializer(points, many=True)
#         total_points = request.user.loyalty_points
#         return Response({
#             'history': serializer.data,
#             'total_points': total_points
#         })