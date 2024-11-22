from typing import Any
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinLengthValidator
from users.validators import validate_name, validate_username
from users.managers import CustomUserManager


class UserType(models.TextChoices):
    ADMIN = 'admin', _('Admin')
    CLIENT = 'client', _('Client')


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model to handle different user types.
    """
    first_name = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("First Name"), validators=[validate_name, MinLengthValidator(3)])
    last_name = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("Last Name"), validators=[validate_name, MinLengthValidator(3)])
    username = models.CharField(
        max_length=150, unique=True, verbose_name=_("Username"), validators=[validate_username, MinLengthValidator(3)])
    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    user_type = models.CharField(
        _('User Type'), max_length=10, choices=UserType.choices, default='admin', db_index=True)
    is_active = models.BooleanField(
        default=True, verbose_name=_("Active"), db_index=True)
    is_staff = models.BooleanField(
        default=False, verbose_name=_("Staff Status"))
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_("Date Joined"))

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        verbose_name=_("Groups"),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True,
        verbose_name=_("User Permissions"),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
