from users.models import Customer
from django.db import models
from products.models import Stock
from django.utils import timezone


class Booking(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)

    # quantity = models.IntegerField(default=1)
    platform = models.CharField(max_length=50, default="")
    date_added = models.DateTimeField(default=timezone.now)
    is_arrived = models.BooleanField(default=False)
    is_picked_up = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + "_" + str(self.date_added)
