import datetime

import jwt
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from api.filters import UsersFilter
from api.serializers.users import (CustomUserCreateSerializer, LoginSerializer,
                                   UserSerializer)
from api.tasks import send_email
from manufacture.settings import (EMAIL_HOST_USER, JWT_REGISTRATION_TTL,
                                  SECRET_KEY, SITE_NAME)
from users.models import CustomUser


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача пользователей с фильтрацией',
    tags=['Пользователи'],
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='Выдача пользователя по ID',
    tags=['Пользователи'],
))
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление пользователей."""

    queryset = CustomUser.objects.all().filter(
        is_active=True
    ).order_by('username')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = UsersFilter

    @method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_description='Выдача информации о залогиненом пользователе',
        tags=['Пользователи'],
    ))
    @action(
        methods=('get',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=CustomUserCreateSerializer,
    responses={400: 'errors', 200: 'OK'},
    tags=['Аутентификация и авторизация'],
)
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
        send_email.delay(
            subject, [recipient], EMAIL_HOST_USER, message=message
        )
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    tags=['Аутентификация и авторизация'],
)
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


@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={400: 'errors', 201: 'access: "token"'},
    tags=['Аутентификация и авторизация'],
)
@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
