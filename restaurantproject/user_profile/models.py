from django.db import models
from users.models import Customer, NewUser

class Profile(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, blank=True, null=True, to_field='email')
    # profile_picture = models.ImageField(default="default_profile_pic.png", null=True, blank=True)
    username = models.CharField(max_length=50, default="Anon", blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    post_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "profile__" + str(self.user)


# class Post(models.Model):
#     author = models.ForeignKey(NewUser, models.CASCADE, blank=True, null=True, to_field='email')
#     content = models.TextField(max_length=1000)
#     likes = models.ManyToManyField(Customer, related_name='post_likes')
#     date_posted = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.author) + "_" + str(self.date_posted)

# class Friend(models.Model):
#     email_1 = models.ForeignKey(NewUser, models.CASCADE, to_field='email', related_name='friend_request_sender')
#     email_2 = models.ForeignKey(NewUser, models.CASCADE, to_field='email', related_name='friend_request_receiver')
#     status = models.CharField(max_length=50, choices=[
#         ('requested', 'requested'),
#         ('confirmed', 'confirmed'),
#         ('none', 'none'),
#     ])

#     def __str__(self):
#         return str(self.email_1) + "__" + str(self.email_2)

# class PostData(models.Model):
#     post = models.ForeignKey(Post, models.CASCADE)
#     comment = models.TextField(max_length=500)

# class Notification(models.Model):
#     sender = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notif_receiver')
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

#     notification_type = models.CharField(max_length=50,choices=[
#         ('FR','friend request'),
#         ('LP', 'like post'),
#         ('PC', 'post comment'),
#     ])
#     complete = models.BooleanField(default=False)

#     def __str__(self):
#         return self.sender.full_name + "_to_" + self.receiver.full_name + "_" + self.notification_type


