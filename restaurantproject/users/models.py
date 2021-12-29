from django.utils import timezone
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class NewUserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError("You must provide an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()

        if other_fields.get('is_superuser') == True:
            group, created = Group.objects.get_or_create(name='admin')
            user.groups.add(group.id)
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
    email = models.EmailField('email', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = NewUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Customer(NewUser):
    phone_number = models.CharField(max_length=10, default="0000000000")
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email