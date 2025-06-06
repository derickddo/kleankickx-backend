# from django.db import models
# from users.models import CustomUser
# from services.models import Service

# class Cart(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
#     session_id = models.CharField(max_length=100, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)