from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, user_create, user_registration, user_login

app_name = 'api'
router = DefaultRouter()

router.register('users', UserViewSet)

urlpatterns = [
    # path('', include('djoser.urls')),
    path('v1/', include(router.urls)),  # разобраться с api/v1/users/me/
    path('v1/auth/user-registration/', user_registration),
    path('v1/auth/activation/<token>/', user_create),
    path('v1/auth/login/', user_login),
    # path(r'auth/', include('djoser.urls.authtoken')),
]
