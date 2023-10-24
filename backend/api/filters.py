from django.db.models import Q
from django_filters import rest_framework as filters

from cars.models import Car, Components
from users.models import CustomUser


class UsersFilter(filters.FilterSet):
    email = filters.CharFilter(method='get_email')
    username = filters.CharFilter(method='get_username')

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def get_email(self, qs, name, value):
        return qs.filter(
            Q(email__istartswith=value) | Q(email__icontains=value)
        )

    def get_username(self, qs, name, value):
        return qs.filter(
            Q(username__istartswith=value) | Q(username__icontains=value)
        )


class ComponentsFilter(filters.FilterSet):
    name = filters.CharFilter(
        method='get_name',
    )
    manufacturer_country = filters.CharFilter(
        field_name='manufacturer_country',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Components
        fields = ('name', 'manufacturer_country')

    def get_name(self, qs, name, value):
        return qs.filter(
            Q(name__istartswith=value) | Q(name__icontains=value)
        )


class CarsFilter(filters.FilterSet):
    employee_first_name = filters.CharFilter(
        field_name='employee__first_name',
        lookup_expr='istartswith',
    )
    employee_last_name = filters.CharFilter(
        field_name='employee__last_name',
        lookup_expr='istartswith',
    )
    creation_date = filters.NumberFilter(
        field_name='creation_date',
        lookup_expr='year__exact',
    )
    creation_date_gt = filters.NumberFilter(
        field_name='creation_date',
        lookup_expr='year__gte',
    )
    creation_date_lt = filters.NumberFilter(
        field_name='creation_date',
        lookup_expr='year__lte',
    )
    body_type = filters.CharFilter(
        field_name='car_body__type',
        lookup_expr='istartswith',
    )
    color = filters.CharFilter(
        field_name='car_body__color',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Car
        fields = (
            'employee_first_name',
            'employee_last_name',
            'creation_date',
            'creation_date_gt',
            'creation_date_lt',
            'car_body',
            'color',
        )
