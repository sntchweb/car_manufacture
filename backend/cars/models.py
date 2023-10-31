import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser

MIN_COMPONENTS_VALUE = 1
MAX_COMPONENTS_VALUE = 32767


class CarBody(models.Model):
    """Модель типа кузова."""

    type = models.CharField(
        verbose_name='Тип кузова',
        max_length=150,
    )
    color = models.CharField(
        verbose_name='Цвет кузова',
        max_length=150,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )

    class Meta:
        verbose_name = 'Кузов'
        verbose_name_plural = 'Кузова'
        ordering = ('type', )

    def __str__(self):
        return self.type


class Components(models.Model):
    """Модель деталей."""

    name = models.CharField(
        verbose_name='Деталь',
        max_length=150,
    )
    manufacturer_country = models.CharField(
        verbose_name='Страна производитель',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Car(models.Model):
    """Модель автомобиля."""

    employee = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name='Сотрудник',
        related_name='cars',
    )
    car_body = models.ForeignKey(
        CarBody,
        on_delete=models.PROTECT,
        verbose_name='Кузов',
        related_name='cars',
    )
    creation_date = models.DateTimeField(
        verbose_name='Дата производства',
        auto_now_add=True,
    )
    сomponents = models.ManyToManyField(
        Components,
        verbose_name='Детали',
        through='CarComponents',
    )
    vin_code = models.UUIDField(
        verbose_name='VIN-код кузова',
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ('-creation_date', )

    # def __str__(self):
    #     return self.car_body


class CarComponents(models.Model):
    """Связующая модель автомобиля и деталей."""

    car = models.ForeignKey(
        Car,
        on_delete=models.PROTECT,
        verbose_name='Автомобиль',
        related_name='car_components',
    )
    component = models.ForeignKey(
        Components,
        on_delete=models.PROTECT,
        verbose_name='Деталь',
        related_name='car_components',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество деталей',
        validators=(
            MinValueValidator(
                MIN_COMPONENTS_VALUE,
                message='Количество деталей не может быть меньше 1'
            ),
            MaxValueValidator(
                MAX_COMPONENTS_VALUE,
                message='Количество деталей не может быть больше 32767'
            )
        )
    )

    class Meta:
        verbose_name = 'Комплектация'
        verbose_name_plural = 'Комплектации'
        ordering = ('car', )

    def __str__(self):
        return f'В автомобиле {self.car} - {self.component} {self.amount} шт.'
