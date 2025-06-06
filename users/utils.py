import logging
from .models import CustomUser, Discount

logger = logging.getLogger(__name__)

def apply_discount_eligibility(user):
    """
    Set signup discount eligibility for a user.
    
    Args:
        user (CustomUser): The user to set discount eligibility for.
    
    Returns:
        None
    """
    try:
        signup_discount = Discount.objects.filter(discount_type='signup', is_active=True).first()
        if signup_discount and not user.signup_discount_applied:
            user.signup_discount_applied = True
            user.save()
            logger.info("Signup discount eligibility set for %s", user.email)
    except Exception as e:
        logger.error("Error setting discount eligibility for %s: %s", user.email, str(e))
        raise