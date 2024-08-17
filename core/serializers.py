

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import OTP
from .utils import send_otp_email

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False 
        user.save()

      
        otp = OTP.objects.create(user=user)
        
       
        send_otp_email(user, otp.otp_code)
        
        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp_code = data.get('otp_code')

        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.get(user=user)
            if not otp.is_valid() or otp.otp_code != otp_code:
                raise serializers.ValidationError('Invalid or expired OTP.')
            return data
        except (User.DoesNotExist, OTP.DoesNotExist):
            raise serializers.ValidationError('Invalid email or OTP.')

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.is_verified = True
        user.is_active = True 
        user.save()
        OTP.objects.filter(user=user).delete() 





class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid login credentials.')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified.')

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }