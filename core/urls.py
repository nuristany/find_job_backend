from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
     path('login/', LoginAPIView.as_view(), name='login'),
]
