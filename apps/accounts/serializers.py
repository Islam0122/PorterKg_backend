from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import GuestProfile, DriverProfile, Car, CarImage
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=['guest', 'driver'], required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        role = validated_data.pop('role')

        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=role,
            auth_type='local'
        )

        # Создаем профиль в зависимости от роли
        if role == 'guest':
            GuestProfile.objects.create(user=user)
        elif role == 'driver':
            DriverProfile.objects.create(
                user=user,
                phone_number='',
                driver_license_number='',
                driver_license_category=''
            )

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'auth_type']
        read_only_fields = ['id', 'email', 'role', 'auth_type']


class GuestProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GuestProfile
        fields = ['id', 'user', 'avatar', 'bio', 'phone_number', 'birth_date', 'created']
        read_only_fields = ['id', 'user', 'created']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'created']
        read_only_fields = ['id', 'created']


class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'marka', 'model', 'color', 'year', 'number_plate',
            'vin_code', 'fuel_type', 'max_passengers', 'description',
            'images', 'created', 'modified'
        ]
        read_only_fields = ['id', 'created', 'modified']


class DriverProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    class Meta:
        model = DriverProfile
        fields = [
            'id', 'user', 'phone_number', 'bio', 'rating', 'experience_years',
            'verified_driver', 'driver_license_number', 'driver_license_category',
            'car', 'created'
        ]
        read_only_fields = ['id', 'user', 'rating', 'verified_driver', 'created']


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()