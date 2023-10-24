from rest_framework import status, viewsets, permissions
from django_filters import rest_framework as filters

from api.filters import CarFilter
from api.serializers.cars import CarSerializer
from cars.models import Car


class CarsViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all().select_related(
        'employee',
        'car_body'
    )
    serializer_class = CarSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = CarFilter
