from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import Address

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,validators=[validate_password()])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','phone_number','date_of_birth',
                  'password','password_confirm')

        def validate(self,attrs):
            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError("Passwords do not  match")
            return attrs

        def create(self,validated_data):
            validated_data.pop('password_confirm')
            password = validated_data.pop('password')
            user = User.objects.create_user(**validated_data)
            user.set_password(password)
            user.save()
            return user

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                 'full_name', 'phone_number', 'date_of_birth', 'is_verified',
                 'date_joined', 'last_login')
        read_only_fields = ('id', 'username', 'is_verified', 'date_joined', 'last_login')
