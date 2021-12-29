from django.db import models
from users.models import Customer, NewUser


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    price = models.IntegerField(default=100)
    type_of = models.CharField(max_length=200, null=False)
    ingredients = models.TextField(null=False)
    description = models.TextField(null=False)
    image = models.URLField(null=False)
    region = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=10)

    def __str__(self):
        return self.product.name + "_" + str(self.quantity)


class ProductReview(models.Model):
    author = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author) + "_" + str(self.product)

class ProductReviewSentiment(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, to_field='email')
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=50, default=None, null=True)

    def __str__(self):
        return str(self.review) + "_" + str(self.sentiment)

# class ProductRating(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     rating = models.IntegerField()

#     def __str__(self):
#         return str(self.customer) + "__" + str(self.product) + "__" + str(self.rating)
