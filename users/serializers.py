from rest_framework import serializers
from .models import CustomUser
from phonenumbers import parse, is_valid_number
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model."""
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number',]

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone_number', 'first_name', 'last_name']

    def validate(self, data):
        
        # Check if email is already in use
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})

        # validate phone if it's a valid phone number using phonenumbers library
        if data.get('phone_number'):  
            try:
                phone_number = parse(data['phone_number'], region='GH')
                if not is_valid_number(phone_number):
                    raise serializers.ValidationError({"phone_number": "Invalid phone number."})
            except Exception as e:
                raise serializers.ValidationError({"phone_number": str(e.args)})       
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


    

class ResendVerificationEmailSerializer(serializers.Serializer):
    """Serializer for resending verification email."""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Check if the email exists in the database."""
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email exists.")
        return value



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to include additional user information in the JWT token."
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name or ''
        token['last_name'] = user.last_name or ''
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data
        