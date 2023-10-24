from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from users.managers import UserManager


class CustomUser(AbstractBaseUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        blank=True,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=150,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-pk', )

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_active and self.is_staff

    def has_perm(self, perm):
        return self.is_active and self.is_staff
