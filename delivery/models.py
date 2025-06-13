# kleankickx-backend/delivery/models.py
from django.db import models

class Delivery(models.Model):
    STATUS_CHOICES = (
        ('PICKED_UP', 'Picked Up'),
        ('CLEANING_ONGOING', 'Cleaning Ongoing'),
        ('READY', 'Ready'),
        ('SCHEDULED_FOR_DELIVERY', 'Scheduled for Delivery'),
        ('DELIVERED', 'Delivered'),
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PICKED_UP')
    delivery_cost = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery {self.id} - {self.status}"
    class Meta:
        db_table = 'delivery'
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),  # Index for status and created_at for faster queries
            models.Index(fields=['id']),  # Index for id for faster lookups
        ]