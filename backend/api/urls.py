from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.cars import CarsViewSet, ComponentsViewSet
from api.views.users import (UserViewSet, user_create, user_login,
                             user_registration)

app_name = 'api'
router = DefaultRouter()

router.register('users', UserViewSet)
router.register('cars', CarsViewSet)
router.register('components', ComponentsViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/user-registration/', user_registration),
    path('v1/auth/activation/<token>/', user_create),
    path('v1/auth/login/', user_login),
]
