# # addresses/models.py
# from django.db import models
# from users.models import CustomUser
# from phonenumber_field.modelfields import PhoneNumberField

# class Address(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
#     name = models.CharField(max_length=100)  # e.g., "John Doe"
#     phone_number = PhoneNumberField()
#     email = models.EmailField()
#     location = models.CharField(max_length=255)  # Street address or specific location
#     region = models.CharField(max_length=100)
#     landmark = models.CharField(max_length=100, blank=True)
#     latitude = models.FloatField(null=True, blank=True)  # From map selection
#     longitude = models.FloatField(null=True, blank=True)  # From map selection
#     is_default = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.name} - {self.location}, {self.region}"

#     class Meta:
#         verbose_name_plural = "Addresses"