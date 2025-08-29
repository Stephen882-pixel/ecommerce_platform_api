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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ('id', 'first_name', 'last_name', 'phone_number', 'date_of_birth')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

        def validate(self, attrs):
            user = self.context['request'].user
            address_type = attrs.get('address_type')
            is_default = attrs.get('is_default', False)

            if is_default and self.instance is None:
                existing_default = Address.objects.filter(
                    user=user,
                    address_type=address_type,
                    is_default=True
                ).exists()
                if existing_default:
                    attrs['is_default'] = False

            return attrs