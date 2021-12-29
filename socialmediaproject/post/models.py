from datetime import datetime
from django.db import models
# from django.utils import timezone
from users.models import NewUser
from upload.models import UserUpload

class Post(models.Model):
    op = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email')
    image = models.ForeignKey(UserUpload, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.op)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email')
    is_liked = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email')
    text = models.TextField(max_length=500, blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.user)

class PostCommentLike(models.Model):
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email')
    is_liked = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) + "_" + str(self.post_comment.id)

# class PostCommentSentiment(models.Model):
#     post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
#     user = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email')
#     is_liked = models.BooleanField(default=False)
#     is_disliked = models.BooleanField(default=False)

#     def __str__(self):
#         return str(self.user)
