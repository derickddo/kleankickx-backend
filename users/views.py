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
# from cart.models import Cart, CartItem
from allauth.account.utils import send_email_confirmation
from allauth.account.forms import SignupForm
from allauth.socialaccount.models import SocialAccount, SocialToken
import requests
from allauth.socialaccount.models import SocialApp
from .forms import CustomSignupForm
from .utils import apply_discount_eligibility
from allauth.account.models import EmailAddress




import logging

logger = logging.getLogger(__name__)

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



class ResendVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_verified:
                    # Send verification email using allauth
                    send_email_confirmation(request, user, signup=True)
                    return Response({'message': 'Verification email resent.'})
                return Response({'error': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user:
#             # Merge session-based cart
#             session_id = request.session.session_key
#             if session_id:
#                 session_cart = Cart.objects.filter(session_id=session_id).first()
#                 if session_cart:
#                     user_cart, created = Cart.objects.get_or_create(user=user)
#                     for session_item in session_cart.items.all():
#                         user_cart_item, item_created = CartItem.objects.get_or_create(
#                             cart=user_cart,
#                             service=session_item.service,
#                             defaults={'quantity': session_item.quantity}
#                         )
#                         if not item_created:
#                             user_cart_item.quantity += session_item.quantity
#                             user_cart_item.save()
#                     session_cart.delete()
#                     request.session.pop('session_key', None)
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'user': CustomUserSerializer(user).data,
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh)
#             })
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

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
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Google login attempt with data")
        id_token = request.data.get('access_token')
    
        try:
            # Fetch Google social app
            try:
                app = SocialApp.objects.get(provider='google')
                logger.info("Google social app client_id: %s", app.client_id)
            except SocialApp.DoesNotExist:
                logger.error("Google social app not configured")
                return Response({'error': 'Google social app not configured.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except SocialApp.MultipleObjectsReturned:
                logger.error("Multiple Google social apps found")
                return Response({'error': 'Multiple Google social apps configured.'}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Mock ID token
            if id_token == 'test-token-123':
                user_data = {
                    'email': 'test@gmail.com',
                    'sub': '123456789',
                    'email_verified': True,
                    'aud': app.client_id,
                    'given_name': 'Test',
                    'family_name': 'User'
                }
            else:
                # Validate ID token
                response = requests.get(
                    'https://oauth2.googleapis.com/tokeninfo',
                    params={'id_token': id_token}
                )
                response.raise_for_status()
                user_data = response.json()
                

                if user_data.get('aud') != app.client_id:
                    logger.error("Invalid audience: %s, expected: %s", user_data.get('aud'), app.client_id)
                    return Response({'error': 'Invalid ID token audience.'}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                if not user_data.get('email_verified'):
                    logger.warning("Google email not verified: %s", user_data.get('email'))
                    return Response({'error': 'Email not verified.'}, 
                                    status=status.HTTP_400_BAD_REQUEST)

            # Create or get the user
            email = user_data['email']
            
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': user_data.get('given_name', ''),
                    'last_name': user_data.get('family_name', ''),
                    'is_verified': True,  # Google accounts are verified
                }
            )

            # Apply bonuses
            if created:
                apply_discount_eligibility(user)
                logger.info("Bonuses applied for new user: %s", user.email)

            # Ensure SocialAccount exists
            social_account, sa_created = SocialAccount.objects.get_or_create(
                user=user,
                provider='google',
                defaults={
                    'uid': user_data['sub'],
                    'extra_data': user_data
                }
            )
            if not sa_created:
                social_account.extra_data.update(user_data)
                social_account.save()

            # Link SocialToken
            SocialToken.objects.update_or_create(
                app=app,
                account=social_account,
                defaults={'token': id_token}
            )

            # Complete login
            complete_signup(request, user, email_verification='none', signal_kwargs={}, success_url=None)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            logger.info("Google login successful for user: %s", user.email)

            return Response({
                'user': CustomUserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'Login successful.'
            }, status=status.HTTP_200_OK)

        except requests.HTTPError as e:
            logger.error("Google ID token validation failed: %s", str(e))
            return Response({'error': f'ID token validation failed: {str(e)}'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Google login failed: %s\n%s", str(e), traceback.format_exc())
            return Response({'error': 'Internal server error. Please try again.'}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)