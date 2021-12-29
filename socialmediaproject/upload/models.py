from django.db import models
from users.models import NewUser

def user_directory_path(instance, filename):
    return 'content/{0}/{1}'.format(instance.user.id, filename)

class UserUpload(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email')
    image = models.ImageField(default="abc_0101_11223.svg", upload_to=user_directory_path)
    upload_type = models.CharField(max_length=50, choices=[
        ('profile_pic', 'profile_pic'),
        ('post', 'post'),
        ('default', 'default'),
    ], default="default")
    date_added = models.DateTimeField(auto_now_add=True)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user) + "__" + str(self.image.url)
