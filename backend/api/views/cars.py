from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from api.filters import CarsFilter, ComponentsFilter
from api.serializers.cars import CarSerializer, ComponentsSerializer
from cars.models import Car, Components


class CarsViewSet(viewsets.ModelViewSet):
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


class ComponentsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление деталей."""

    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer
    # permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ComponentsFilter
