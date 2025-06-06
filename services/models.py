# from django.db import models

# # Create your models here.
# class Service(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     image_base64 = models.TextField(blank=True, null=True, help_text="Base64 encoded image data")
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     duration = models.PositiveIntegerField(help_text="Duration in minutes")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name
