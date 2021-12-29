from django.shortcuts import render
from products.models import Product
from users.models import Shop, Customer
import random


def home(request):
    pass
    # context = {'products': []}

    # if request.user.groups.exists():
    #     if request.user.groups.all()[0].name == 'shop':
    #         context['is_shop'] = True
    #         context['name'] = Shop.objects.get(
    #             email=request.user).shop_name
    #     else:
    #         context['name'] = Customer.objects.get(
    #             email=request.user).username

    # # product_ids = random.sample(list(Product.objects.filter(
    #     # can_sell=True).values_list('id', flat=True)), 10)

    # product_ids = list(Product.objects.filter(
    #     can_sell=True).values_list('id', flat=True))

    # for id in product_ids:
    #     product = Product.objects.get(id=id)
    #     context['products'].append({
    #         'id': id,
    #         'name': product.name,
    #         'box_art': product.box_art
    #     })

    # return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'home/about.html')
