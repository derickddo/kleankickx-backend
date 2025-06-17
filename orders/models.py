from django.db import models
from users.models import CustomUser
from services.models import Service
from addresses.models import Address
from payments.models import Payment
from delivery.models import Delivery
import uuid

class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='orders')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, related_name='orders')
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        ordering = ['-created_at'] # Orders are ordered by creation date, most recent first

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.service.name} in Order {self.order.id}"
    class Meta:
        db_table = 'order_item'
        verbose_name = 'Order Item'
      