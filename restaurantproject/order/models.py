from django.db import models
from product.models import Product
from users.models import NewUser

class Order(models.Model):
    user = models.ForeignKey(NewUser, blank=True, null=True, on_delete=models.SET_NULL, to_field='email')
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=(
        ('incomplete', 'incomplete'),
        ('confirmed', 'confirmed'),
        ('complete', 'complete')
    ), default="incomplete")

    def __str__(self):
        return str(self.user) + "_" + str(self.order_date)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL)
    quantity=models.IntegerField(null=True)
    total_price = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order) + "__" + str(self.date_added)