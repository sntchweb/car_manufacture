# Generated by Django 4.1 on 2023-10-25 16:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата производства"
                    ),
                ),
                (
                    "vin_code",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        verbose_name="VIN код кузова",
                    ),
                ),
            ],
            options={
                "verbose_name": "Автомобиль",
                "verbose_name_plural": "Автомобили",
                "ordering": ("-creation_date",),
            },
        ),
        migrations.CreateModel(
            name="CarBody",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=150, verbose_name="Тип кузова")),
                ("color", models.CharField(max_length=150, verbose_name="Цвет кузова")),
                ("slug", models.SlugField(unique=True, verbose_name="Слаг")),
            ],
            options={
                "verbose_name": "Кузов",
                "verbose_name_plural": "Кузова",
                "ordering": ("type",),
            },
        ),
        migrations.CreateModel(
            name="Components",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Деталь")),
                (
                    "manufacturer_country",
                    models.CharField(
                        max_length=150, verbose_name="Страна производитель"
                    ),
                ),
            ],
            options={
                "verbose_name": "Деталь",
                "verbose_name_plural": "Детали",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="CarComponents",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="Количество деталей не может быть меньше 1"
                            ),
                            django.core.validators.MaxValueValidator(
                                32767,
                                message="Количество деталей не может быть больше 32767",
                            ),
                        ],
                        verbose_name="Количество деталей",
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="car_components",
                        to="cars.car",
                        verbose_name="Автомобиль",
                    ),
                ),
                (
                    "component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="car_components",
                        to="cars.components",
                        verbose_name="Деталь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Комплектация",
                "verbose_name_plural": "Комплектации",
                "ordering": ("car",),
            },
        ),
        migrations.AddField(
            model_name="car",
            name="car_body",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="cars",
                to="cars.carbody",
                verbose_name="Кузов",
            ),
        ),
        migrations.AddField(
            model_name="car",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="cars",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Сотрудник",
            ),
        ),
        migrations.AddField(
            model_name="car",
            name="сomponents",
            field=models.ManyToManyField(
                through="cars.CarComponents",
                to="cars.components",
                verbose_name="Детали",
            ),
        ),
    ]