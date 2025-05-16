"""User Models."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User Model."""

    class Meta:
        ordering = ["email"]
        verbose_name = "user"
        verbose_name_plural = "users"

    username = models.CharField(
        verbose_name="Username",
        max_length=32,
        blank=False,
        null=False,
        unique=True,
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=64,
        blank=False,
        null=False,
        unique=True,
    )
