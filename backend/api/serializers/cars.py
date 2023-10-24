from rest_framework import serializers

from api.serializers.users import UserSerializer
from cars.models import Car, CarBody, Components, CarComponents


class ComponentsInCarSerializer(serializers.ModelSerializer):
    """Сериализатор для деталей автомобиля."""

    name = serializers.ReadOnlyField(
        source='component.name'
    )
    manufacturer_country = serializers.ReadOnlyField(
        source='component.manufacturer_country'
    )

    class Meta:
        model = CarComponents
        fields = (
            'name',
            'amount',
            'manufacturer_country',
        )


class CarBodySerializer(serializers.ModelSerializer):
    """Сериализатор для кузова автомобиля."""

    body_type = serializers.StringRelatedField(source='type')

    class Meta:
        model = CarBody
        fields = (
            'type',
            'color',
            'body_type',
            'vin_code',
        )


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор для автомобиля."""

    employee = UserSerializer(read_only=True)
    car_body = CarBodySerializer(read_only=True)
    creation_date = serializers.SerializerMethodField(
        source='get_creation_date',
    )
    components = ComponentsInCarSerializer(
        many=True,
        read_only=True,
        source='car',
    )

    class Meta:
        model = Car
        fields = (
            'car_body',
            'creation_date',
            'components',
            'employee',
        )

    def get_creation_date(self, obj):
        return obj.creation_date.strftime('%Y-%m-%d')
