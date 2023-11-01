from rest_framework import serializers

from api.serializers.users import UserSerializer
from cars.models import Car, CarBody, CarComponents, Components


class ComponentsInCarSerializer(serializers.ModelSerializer):
    """Сериализатор деталей автомобиля."""

    component_name = serializers.ReadOnlyField(source='component.name')
    manufacturer_country = serializers.ReadOnlyField(
        source='component.manufacturer_country'
    )

    class Meta:
        model = CarComponents
        fields = (
            'component_name',
            'amount',
            'manufacturer_country',
        )


class CarBodySerializer(serializers.ModelSerializer):
    """Сериализатор кузова автомобиля."""

    body_type = serializers.StringRelatedField(source='type')

    class Meta:
        model = CarBody
        fields = ('color', 'body_type')


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор автомобиля."""

    employee = UserSerializer(read_only=True)
    vin_code = serializers.SerializerMethodField(source='get_vin_code')
    car_body = CarBodySerializer(read_only=True)
    creation_date = serializers.SerializerMethodField(
        source='get_creation_date',
    )
    components = ComponentsInCarSerializer(
        many=True,
        read_only=True,
        source='car_components',
    )
    total_components_cnt = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = (
            'car_body',
            'vin_code',
            'creation_date',
            'components',
            'total_components_cnt',
            'employee',
        )

    def get_creation_date(self, obj):
        """Возвращает дату сборки автомобиля в формате ГГГГ-ММ-ДД."""

        return obj.creation_date.strftime('%Y-%m-%d')

    def get_vin_code(self, obj):
        """Возвращает VIN-код автомобиля."""

        return ''.join(str(obj.vin_code).split('-')).upper()


class ComponentsSerializer(serializers.ModelSerializer):
    """Сериализатор для деталей."""

    class Meta:
        model = Components
        fields = ('name', 'manufacturer_country')
