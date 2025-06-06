from rest_framework import serializers
from .models import CustomUser
from phonenumbers import parse, is_valid_number

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number',]

class RegisterSerializer(serializers.ModelSerializer):
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
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email exists.")
        return value

        