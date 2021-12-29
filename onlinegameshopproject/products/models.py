from django.db import models
from django.utils import timezone
from users.models import Shop


class Product(models.Model):
    name = models.CharField(max_length=200)
    publisher = models.CharField(max_length=50)
    developer = models.CharField(max_length=50)
    description = models.TextField()
    release_date = models.CharField(max_length=50)
    can_sell = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)
    box_art = models.URLField(default="")
    esrb_rating = models.URLField(default="")

    def __str__(self):
        return self.name


class Stock(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, limit_choices_to={
                                'can_sell': True}, on_delete=models.CASCADE)

    platforms = models.CharField(max_length=500, default="")
    price = models.IntegerField()

    in_stock = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('shop', 'product',)

    def __str__(self):
        return str(self.product) + "_by_" + str(self.shop.shop_name)
