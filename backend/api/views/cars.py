from django.db.models import Sum
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets

from api.filters import CarsFilter, ComponentsFilter
from api.serializers.cars import CarSerializer, ComponentsSerializer
from cars.models import Car, Components


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Выдача автомобилей с фильтрацией",
        tags=["Автомобили"],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Выдача автомобиля по ID",
        tags=["Автомобили"],
    ),
)
class CarsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление автомобилей."""

    queryset = (
        Car.objects.select_related("employee", "car_body")
        .prefetch_related("car_components__component")
        .only(
            "employee__id",
            "employee__username",
            "employee__email",
            "employee__first_name",
            "employee__last_name",
            "car_body__color",
            "car_body__type",
            "vin_code",
            "creation_date",
        )
        .annotate(
            total_components_cnt=Sum("car_components__amount"),
        )
    )
    serializer_class = CarSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarsFilter


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Выдача комплектующих с фильтрацией",
        tags=["Комплектующие"],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Выдача детали по ID",
        tags=["Комплектующие"],
    ),
)
class ComponentsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление деталей."""

    queryset = Components.objects.all().order_by("name")
    serializer_class = ComponentsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ComponentsFilter
