# # users/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from allauth.account.models import EmailAddress
# from .models import CustomUser, BonusTransaction
# import logging
# import traceback


# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=EmailAddress)
# def update_user_verified_and_bonuses(sender, instance, created, **kwargs):
#     try:
#         user = instance.user
#         if created or instance.verified:
#             if not user.is_verified:
#                 user.is_verified = True
#                 # Apply signup bonus
#                 if not BonusTransaction.objects.filter(user=user, bonus_type='signup').exists():
#                     user.loyalty_points += 100
#                     user.signup_discount_used = False
#                     BonusTransaction.objects.create(
#                         user=user, bonus_type='signup', points=100
#                     )
#                     logger.info("Signup bonus applied for %s: 100 points", user.email)
#                 user.save()

#             # Check for referral bonuses
#             if user.referred_by and user.referred_by.is_verified:
#                 if not BonusTransaction.objects.filter(user=user, bonus_type='referral').exists():
#                     user.loyalty_points += 50
#                     BonusTransaction.objects.create(
#                         user=user, bonus_type='referral', points=50
#                     )
#                     logger.info("Referral bonus applied for %s: 50 points", user.email)
#                 if not BonusTransaction.objects.filter(user=user.referred_by, bonus_type='referrer').exists():
#                     user.referred_by.loyalty_points += 100
#                     BonusTransaction.objects.create(
#                         user=user.referred_by, bonus_type='referrer', points=100
#                     )
#                     user.referred_by.save()
#                     logger.info("Referrer bonus applied for %s: 100 points", user.referred_by.email)
#                 user.save()

#             # Check users referred by this user
#             for referred_user in user.referrals.filter(is_verified=True):
#                 if not BonusTransaction.objects.filter(user=referred_user, bonus_type='referral').exists():
#                     referred_user.loyalty_points += 50
#                     BonusTransaction.objects.create(
#                         user=referred_user, bonus_type='referral', points=50
#                     )
#                     referred_user.save()
#                     logger.info("Deferred referral bonus applied for %s: 50 points", referred_user.email)
#                 if not BonusTransaction.objects.filter(user=user, bonus_type='referrer').exists():
#                     user.loyalty_points += 100
#                     BonusTransaction.objects.create(
#                         user=user, bonus_type='referrer', points=100
#                     )
#                     logger.info("Deferred referrer bonus applied for %s: 100 points", user.email)
#             user.save()
#     except Exception as e:
#         logger.error("Signal error: %s\n%s", str(e), traceback.format_exc())
#         raise