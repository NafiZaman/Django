from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError("You must provide an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True.")
        if other_fields.get('is_active') is not True:
            raise ValueError("Superuser must be assigned to is_active=True.")

        return self.create_user(email, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Shop(NewUser):
    shop_name = models.CharField(max_length=200)
    date_joined = models.DateTimeField(default=timezone.now)

    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.shop_name


class Customer(NewUser):
    username = models.CharField(max_length=200)
    date_joined = models.DateTimeField(default=timezone.now)

    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
