from django.contrib.auth.models import AbstractUser
from django.db import models

from distribution.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    verification_token = models.CharField(max_length=100, verbose_name='токен верификации', **NULLABLE )
    is_verificated = models.BooleanField(default=False, verbose_name='верификация')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            (
                'set_active',
                'Activate/deactivate user'
            )
        ]