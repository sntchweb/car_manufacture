import jwt
from rest_framework import authentication, exceptions

from manufacture.settings import SECRET_KEY
from users.models import CustomUser

AUTHENTICATION_ERROR_MSG = ('Ошибка аутентификации. '
                            'Невозможно декодировать токен!')
USER_NOT_FOUND_ERROR_MSG = ('Пользователь соответствующий '
                            'данному токену не найден!')
USER_DEACTIVATED_MSG = 'Пользователь деактивирован!'


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        if not auth_header:
            return None
        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')
        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except Exception:
            raise exceptions.AuthenticationFailed(AUTHENTICATION_ERROR_MSG)
        try:
            user = CustomUser.objects.get(pk=payload['user_id'])
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed(USER_NOT_FOUND_ERROR_MSG)
        if not user.is_active:
            raise exceptions.AuthenticationFailed(USER_DEACTIVATED_MSG)
        return user, token
