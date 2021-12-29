from django.db import models
from users.models import NewUser
from upload.models import UserUpload

class Profile(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, to_field='email')
    profile_pic = models.ForeignKey(UserUpload, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True, default="")
    education = models.CharField(max_length=250, blank=True, null=True, default="")

    rel_status = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('single', 'single'),
        ('engaged', 'engaged'),
        ('married', 'married'),
    ])

    work = models.CharField(max_length=250, blank=True, null=True, default="")
    location = models.CharField(max_length=250, blank=True, null=True, default="")

    # interests = models.TextField(max_length=500, blank=True, null=True)
    # profile_pic = models.ImageField(default="abc_0101_11223.svg", upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return str(self.user)
