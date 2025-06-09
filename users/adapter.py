
from allauth.account.adapter import DefaultAccountAdapter
from .utils import apply_discount_eligibility
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Construct verification URL pointing to frontend.
        """
        # Use frontend URL with the confirmation key
        url = f"http://localhost:5173/verify-email/{emailconfirmation.key}"
        return url
  

    def respond_email_verification_sent(self, request, user):
        """
        Return JSON response for email verification sent.
        """
        return Response({
            'message': 'Verification email sent. Please check your email.'
        }, status=200)

    
    
    