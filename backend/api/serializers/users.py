import datetime

import jwt
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from manufacture.settings import JWT_ACCESS_TTL, SECRET_KEY
from users.models import CustomUser

AUTHENTICATION_ERROR_MESSAGE = 'email или пароль введены неверно'
USER_DOES_NOT_EXISTS_MESSAGE = 'Пользователя с таким email не существует'


class UserSerializer(serializers.ModelSerializer):
    total_cars_created = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'total_cars_created',
        )


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def validate(self, data):
        validate_password(data['password'])
        return data


class LoginSerializer(serializers.Serializer):
    """Сериализатор для авторизации пользователей."""

    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data['email']
        password = validated_data['password']
        try:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError(AUTHENTICATION_ERROR_MESSAGE)
            validated_data['user'] = user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(USER_DOES_NOT_EXISTS_MESSAGE)
        return validated_data

    def create(self, validated_data):
        user_id = str(validated_data['user'].id)
        access_payload = {
            'iss': 'backend-api',
            'user_id': user_id,
            'exp': datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(seconds=JWT_ACCESS_TTL),
            'type': 'access',
        }
        access = jwt.encode(access_payload, SECRET_KEY)
        return {'access': access}
