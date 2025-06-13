from django.urls import path, include
from .views import RegisterView, ResendEmailVerificationView, GoogleLoginView, GetCSRFTokenView, CustomConfirmEmailView, CartView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('google-login/', GoogleLoginView.as_view(), name='google_login'),
    path('cart/', CartView.as_view(), name='cart'),
    path('resend-verification-email/', ResendEmailVerificationView.as_view(), name='resend_verification_email'),
    path('get-csrf-token/', GetCSRFTokenView.as_view(), name='get_csrf_token'),
    path('verify-email/<str:key>/', CustomConfirmEmailView.as_view(), name='verify_email'),
]