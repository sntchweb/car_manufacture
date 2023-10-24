import datetime

import jwt
from django_filters import rest_framework as filters
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.filters import UsersFilter
from api.tasks import send_email
from manufacture.settings import (EMAIL_HOST_USER, JWT_REGISTRATION_TTL,
                                  SECRET_KEY, SITE_NAME)
from users.models import CustomUser
from api.serializers.users import (CustomUserCreateSerializer, UserSerializer,
                                   LoginSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Представление пользователей."""

    queryset = CustomUser.objects.all().order_by('username')
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = UsersFilter


@api_view(['POST'])
def user_registration(request):
    serializer = CustomUserCreateSerializer(data=request.data)
    if serializer.is_valid():
        payload = {"exp": datetime.datetime.now(
            tz=datetime.timezone.utc) + datetime.timedelta(
                JWT_REGISTRATION_TTL)
        }
        payload.update(serializer.data)
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        subject = 'Активация аккаунта на сайте'
        message = ('Для завершения регистрации на сайте '
                   'перейдите по ссылке: '
                   f'{SITE_NAME}/api/v1/auth/activation/{encoded_jwt}/')
        recipient = serializer.data['email']
        send_email(
            subject, [recipient], EMAIL_HOST_USER, message=message
        )
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_create(request, token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        serializer = CustomUserCreateSerializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.data
            CustomUser.objects.create_user(**validated_data, is_active=True)
            return Response(
                'Аккаунт успешно создан!',
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except jwt.ExpiredSignatureError:
        return Response(
            'Срок действия ссылки истек', status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
