from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets

from api.filters import CarsFilter, ComponentsFilter
from api.serializers.cars import CarSerializer, ComponentsSerializer
from cars.models import Car, Components


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача автомобилей с фильтрацией',
    tags=['Автомобили'],
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='Выдача автомобиля по ID',
    tags=['Автомобили'],
))
class CarsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление автомобилей."""

    queryset = Car.objects.select_related(
        'employee',
        'car_body',
    ).prefetch_related(
        'car_components',
    )
    serializer_class = CarSerializer
    # permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarsFilter


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача деталей с фильтрацией',
    tags=['Детали'],
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='Выдача детали по ID',
    tags=['Детали'],
))
class ComponentsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление деталей."""

    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer
    # permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ComponentsFilter
