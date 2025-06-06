# from django.db import models
# from users.models import CustomUser
# from orders.models import Order

# class LoyaltyPoint(models.Model):
#     SOURCE_CHOICES = (
#         ('ORDER', 'Order'),
#         ('REFERRAL', 'Referral'),
#         ('SIGNUP', 'Signup'),
#         ('PROMOTION', 'Promotion'),
#     )

#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     points = models.PositiveIntegerField()
#     source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
#     order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.points} points for {self.user.username} ({self.source})"