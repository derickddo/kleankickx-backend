
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

    def confirm_email(self, request, email_address):
        """
        Verify email, apply signup discount, and log in the user.
        """
        super().confirm_email(request, email_address)
        user = email_address.user
        user.is_verified = True
        user.save()
        apply_discount_eligibility(user)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        logger.info("Email verified, discount applied, and user logged in for %s", user.email)

        # Store tokens in request for response
        request.jwt_tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    def respond_email_verification_sent(self, request, user):
        """
        Return JSON response for email verification sent.
        """
        return Response({
            'message': 'Verification email sent. Please check your email.'
        }, status=200)

    def respond_email_confirmation(self, request, email_address):
        """
        Return JSON response with JWT tokens after verification.
        """
        return Response({
            'message': 'Email verified successfully.',
            'user': {
                'id': str(email_address.user.id),
                'email': email_address.user.email,
                'first_name': email_address.user.first_name,
                'last_name': email_address.user.last_name,
                'is_verified': email_address.user.is_verified,
                'signup_discount_applied': email_address.user.signup_discount_applied
            },
            'access': request.jwt_tokens['access'],
            'refresh': request.jwt_tokens['refresh']
        }, status=200)