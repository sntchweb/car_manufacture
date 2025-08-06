from rest_framework import serializers

from api.serializers.users import UserSerializer
from cars.models import Car, CarBody, CarComponents, Components


class ComponentsSerializer(serializers.ModelSerializer):
    """Сериализатор для деталей."""

    class Meta:
        model = Components
        fields = ("id", "name", "manufacturer_country")


class ComponentsInCarSerializer(serializers.ModelSerializer):
    """Сериализатор деталей автомобиля."""

    # component_name = serializers.ReadOnlyField(source='component.name')
    component = ComponentsSerializer(read_only=True)

    class Meta:
        model = CarComponents
        fields = ("amount", "component")


class CarBodySerializer(serializers.ModelSerializer):
    """Сериализатор кузова автомобиля."""

    body_type = serializers.StringRelatedField(source="type")

    class Meta:
        model = CarBody
        fields = ("id", "color", "body_type")


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор автомобиля."""

    employee = UserSerializer(read_only=True)
    vin_code = serializers.SerializerMethodField(source="get_vin_code")
    car_body = CarBodySerializer(read_only=True)
    creation_date = serializers.DateTimeField(format="%d-%m-%Y")
    components = ComponentsInCarSerializer(
        many=True,
        read_only=True,
        source="car_components",
    )
    total_components_cnt = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = (
            "id",
            "car_body",
            "vin_code",
            "creation_date",
            "components",
            "total_components_cnt",
            "employee",
        )

    def get_vin_code(self, obj):
        """Возвращает VIN-код автомобиля."""

        return str(obj.vin_code).replace("-", "").upper()
