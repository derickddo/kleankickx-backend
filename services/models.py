# services/models.py
from django.db import models

class Service(models.Model):
    """Model representing a service offered by the application."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.BinaryField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        db_table = 'services'
        ordering = ['-created_at']
