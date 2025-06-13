import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from allauth.account.utils import complete_signup
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .serializers import CustomUserSerializer, RegisterSerializer, ResendVerificationEmailSerializer
from .models import CustomUser
from services.models import Service
# from cart.models import Cart, CartItem
from allauth.account.utils import send_email_confirmation
from allauth.account.forms import SignupForm
from allauth.socialaccount.models import SocialAccount, SocialToken
import requests
from allauth.socialaccount.models import SocialApp
from .forms import CustomSignupForm
from .utils import apply_discount_eligibility
from allauth.account.models import EmailAddress
from django.middleware.csrf import get_token
from allauth.account.models import EmailConfirmationHMAC





import logging

logger = logging.getLogger(__name__)

class GetCSRFTokenView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrf_token': csrf_token}, status=status.HTTP_200_OK)

class CustomConfirmEmailView(APIView):
    permission_classes = [AllowAny]
    """Custom email confirmation view to handle email verification links.
    This view uses the EmailConfirmationHMAC from allauth to verify the email address.
    It also applies discount eligibility and logs the user in after verification.
    """
    def post(self, request, key, *args, **kwargs):
        try:
            confirmation = EmailConfirmationHMAC.from_key(key)
            if confirmation is None:
                return Response({'error': 'Invalid or expired confirmation link.'}, status=400)
          
            email_address = confirmation.email_address
            if email_address.verified:
                return Response({'error': 'Email already verified.'}, status=400)

            confirmation.confirm(request)
            # Optional: perform signup login step
            user = email_address.user
            user.is_verified = True
            user.save()
            apply_discount_eligibility(user)
            logger.info("Email verified, discount applied, for %s", user.email)

            # Return success response with tokens
            return Response({
                'message': 'Email verified successfully.',
                
            }, status=200)

        except Exception:
            return Response({'error': 'Verification failed. The link may be expired or invalid.'}, status=400)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Invalid registration data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        first_name = serializer.validated_data.get('first_name', '')
        last_name = serializer.validated_data.get('last_name', '')
        phone_number = serializer.validated_data.get('phone_number', None)

        try:
            if CustomUser.objects.filter(email=email).exists():
                logger.warning("Email already exists: %s", email)
                return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                is_verified=False
            )

            # Create unverified email address
            EmailAddress.objects.create(
                user=user,
                email=email,
                primary=True,
                verified=False
            )

            # Trigger allauth email verification
            user.emailaddress_set.filter(email=email).first().send_confirmation(request)

            logger.info("Registration successful, verification email sent to %s", email)
            return Response({
                'message': 'Registration successful. Please check your email to verify your account.'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("Registration failed for %s: %s\n%s", email, str(e), traceback.format_exc())
            return Response({'error': 'Registration failed. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ResendEmailVerificationView(APIView):
    """ View to resend email verification link to users who have not verified their email.
    This view checks if the user exists and if their email is already verified.
    If the email is not verified, it sends a new verification email using allauth's email confirmation system.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_verified:
                return Response({'message': 'Email already verified.'}, status=status.HTTP_200_OK)

            # Trigger allauth email verification
            email_address = user.emailaddress_set.filter(email=email).first()
            if email_address:
                email_address.send_confirmation(request)
                return Response({'message': 'Verification email sent.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Email address not found.'}, status=status.HTTP_404_NOT_FOUND)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    """Login view to authenticate users using email and password.
    """
    def post(self, request):        
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            refresh['email'] = user.email
            refresh['first_name'] = user.first_name or ''
            refresh['last_name'] = user.last_name or ''
            refresh['is_verified'] = user.is_verified

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]



    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token})
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)




class GoogleLoginView(APIView):
    """Google login view to authenticate users using Google OAuth2."""
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get('token')
        if not access_token:
            return Response({'error': 'No access token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.get(
                f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={access_token}"
            )
            if response.status_code != 200:
                return Response({'error': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)
            
            token_data = response.json()
            email = token_data.get('email')
            if not email:
                return Response({'error': 'Email not provided by Google'}, status=status.HTTP_400_BAD_REQUEST)

            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': token_data.get('given_name', ''),
                    'last_name': token_data.get('family_name', ''),
                    'is_active': True
                }
            )

            if created:
                logger.info("New user created via Google login: %s", email)

                # Apply discount eligibility for new users
                apply_discount_eligibility(user)

            else:
                logger.info("Existing user logged in via Google: %s", email)

            refresh = RefreshToken.for_user(user)
            refresh['email'] = user.email
            refresh['first_name'] = user.first_name or ''
            refresh['last_name'] = user.last_name or ''
            refresh['is_verified'] = user.is_verified
            logger.info("Google login successful for user: %s", email)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'Google login successful'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Google login error: %s", str(e))
            return Response({'error': 'Google login failed'}, status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'cart': request.user.cart_data}, status=status.HTTP_200_OK)

    def post(self, request):
        cart = request.data.get('cart', [])
        for item in cart:
            try:
                Service.objects.get(id=item['service_id'])
            except Service.DoesNotExist:
                return Response({'error': f"Service {item['service_id']} not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.cart_data = cart
        request.user.save()
        logger.info(f"Updated cart for user {request.user.email}")
        return Response({'cart': cart}, status=status.HTTP_200_OK)