# from django.db import models
# from users.models import CustomUser
# from phonenumber_field.modelfields import PhoneNumberField

# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('PICKED_UP', 'Picked Up'),
#         ('CLEANING_ONGOING', 'Cleaning Ongoing'),
#         ('READY', 'Ready'),
#         ('SCHEDULED', 'Scheduled for Delivery'),
#         ('DELIVERED', 'Delivered'),
#     )

#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # New field
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PICKED_UP')
#     delivery_name = models.CharField(max_length=100)
#     delivery_phone = PhoneNumberField()
#     delivery_email = models.EmailField()
#     delivery_address = models.TextField()
#     delivery_region = models.CharField(max_length=100)
#     delivery_landmark = models.CharField(max_length=100, blank=True)
#     delivery_latitude = models.FloatField(null=True, blank=True)
#     delivery_longitude = models.FloatField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)