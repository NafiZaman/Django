from django.db import models
from django.utils import timezone
from users.models import NewUser

class Friend(models.Model):
    sender = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email', related_name="sender")
    receiver = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email', related_name="receiver")
    confirmed = models.BooleanField(default=False)
    date_added = models.DateField(default=timezone.now)

    unique_together = [['receiver', 'sender'], ['sender', 'receiver']]

    def __str__(self):
        return str(self.sender) + "__" + str(self.receiver)