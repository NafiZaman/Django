from django.shortcuts import render
from .models import Product, Stock
from users.models import Customer, Shop
from difflib import SequenceMatcher


def view_product(request, product_id):
    print(product_id)
    context = {}

    try:
        product = Product.objects.get(id=product_id)
        context['product'] = {
            'name': product.name,
            'box_art': product.box_art,
            'esrb_rating': product.esrb_rating,
            'description': product.description,
            'publisher': product.publisher,
            'developer': product.developer,
            'release_date': product.release_date,
        }

        stocks = Stock.objects.filter(
            product_id=product.id)

        context['stocks'] = []

        for stock in stocks:
            shop = Shop.objects.get(id=stock.shop.id)
            context['stocks'].append({
                'id': stock.id,
                'name': shop.shop_name,
                'price': stock.price,
                'address': str(shop.city)+", "+str(shop.country)+", "+str(shop.zipcode),
                'phone': shop.phone,
                'in_stock': stock.in_stock,
                'platforms': stock.platforms,
            })

    except Exception as e:
        print("ERROR! ", e)
        context['is_server_error'] = True

    return render(request, 'products/product.html', context)


def featured_products(request):
    context = {'products': []}

    if request.user.groups.exists():
        if request.user.groups.all()[0].name == 'shop':
            context['is_shop'] = True
            context['name'] = Shop.objects.get(
                email=request.user).shop_name
        else:
            context['name'] = Customer.objects.get(
                email=request.user).username

    if request.method == 'GET':
        # product_ids = []
        if 'search' in request.GET and request.GET.get('search'):
            search_item = request.GET.get('search')
            products = Product.objects.filter(
                name__istartswith=search_item[0])

            for p in products:
                if SequenceMatcher(None, search_item, p.name.lower()).ratio() > 0.2:
                    context['products'].append({
                        'id': p.id,
                        'name': p.name,
                        'release_date': p.release_date,
                        'box_art': p.box_art
                    })
                # print('{}, {} similarity score: {}'.format(search_item, p.name, SequenceMatcher(
                #     None, search_item, p.name.lower()).ratio()))

        else:
            products = Product.objects.raw(
                'SELECT * FROM products_product WHERE id IN (SELECT id FROM products_product ORDER BY RANDOM() LIMIT 20)')

            for p in products:
                context['products'].append({
                    'id': p.id,
                    'name': p.name,
                    'release_date': p.release_date,
                    'box_art': p.box_art
                })

    return render(request, 'products/featured_products.html', context)
