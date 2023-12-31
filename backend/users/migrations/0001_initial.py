# Generated by Django 4.1 on 2023-10-25 16:10

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Имя пользователя",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Имя"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Фамилия"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=150, unique=True, verbose_name="Электронная почта"
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "ordering": ("-pk",),
            },
        ),
    ]
