from django.urls import path, include
from .views import RegisterView, ResendVerificationView, GoogleLoginView

urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('google/login', GoogleLoginView.as_view(), name='google_login'),
    path('resend-verification-email', ResendVerificationView.as_view(), name='resend_verification_email'),

]