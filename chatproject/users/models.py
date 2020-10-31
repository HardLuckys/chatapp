from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.conf import settings


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, null=True, max_length=15, verbose_name="username")
    email = models.EmailField(unique=True,  null=True, verbose_name="емайл")
    created_at = models.DateTimeField(default=datetime.now, verbose_name="создан в")
    slug = models.SlugField(unique=True, null=True, verbose_name="ID (айди)")
    avatar = models.ImageField(upload_to='media', default='media/icon-user-default.png', verbose_name="автарка")
