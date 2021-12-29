from datetime import date
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group

class CustomerAccountManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError("You must provide an email address")
        
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
        other_fields.setdefault('first_name', "")
        other_fields.setdefault('last_name', "")
        other_fields.setdefault('dob', date.today())
        other_fields.setdefault('gender', 'other')

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")
        if other_fields.get('is_active') is not True:
            raise ValueError("Superuser must be assigned to is_active=True.")

        return self.create_user(email, password, **other_fields)

class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    dob = models.DateField()
    gender = models.CharField(null=False, blank=False, max_length=10, choices=[
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),
    ])
    date_joined = models.DateTimeField(default=timezone.now)
    full_name = models.CharField(max_length=300, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomerAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class UserSetting(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, to_field='email')
    post_visibility = models.CharField(max_length=50, blank=False, null=False, choices=[
        ('public', 'public'),
        ('friends', 'friends'),
        ('private', 'private'),
    ], default="friends")

    profile_visibility = models.CharField(max_length=50, blank=False, null=False, choices=[
        ('public', 'public'),
        ('friends', 'friends'),
        ('private', 'private'),
    ], default="friends")

    upload_visibility = models.CharField(max_length=50, blank=False, null=False, choices=[
        ('public', 'public'),
        ('friends', 'friends'),
        ('private', 'private'),
    ], default="friends")

    def __str__(self):
        return str(self.user)

# class Notification(models.Model):
#     receiver = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email', related_name='notif_receiver')
#     sender = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email', related_name='notif_sender')
#     notif_type = models.CharField(max_length=100, choices=[
#         ('accepted_request', 'accepted_request'),
#         ('received_request', 'received_request'),
#         ('post_comment', 'post_comment'),
#         # ('post_like', 'post_like'),
#         # ('comment_like', 'comment_like')
#     ])

#     date_added = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return str(self.notif_type)
    

def user_directory_path(instance, filename):
    return 'content/{0}/profile_pic/{1}'.format(instance.id, filename)