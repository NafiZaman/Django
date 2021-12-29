from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.models import *
from users.decorators import allowed_users
from products.models import *
from products.forms import AddNewProductForm, UpdateShopProductForm


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['shop'])
def my_products(request):
    context = {'products': []}

    try:
        shop = Shop.objects.get(email=request.user)
        context['shop_name'] = shop.shop_name

        if request.method == 'POST':
            if 'update' in request.POST:
                form = UpdateShopProductForm(request.POST)

                if form.is_valid():
                    # print(request.POST)
                    product_id = request.POST.get('update')

                    stock = Stock.objects.get(shop=shop.id, product=product_id)
                    stock.price = form.cleaned_data.get('price')
                    stock.in_stock = form.cleaned_data.get('in_stock')
                    stock.platforms = ', '.join(
                        form.cleaned_data.get('platforms'))

                    stock.save()

            elif 'remove' in request.POST:
                stock = Stock.objects.filter(
                    shop=shop.id, product=request.POST.get('remove'))

                if stock.exists():
                    stock.delete()

            return HttpResponseRedirect(reverse('user_profile:my_products'))

        product_ids = Stock.objects.filter(
            shop=shop.id).values_list('product', flat=True)

        for id in product_ids:
            product = Product.objects.get(pk=id)
            stock = Stock.objects.get(shop=shop.id, product=id)
            prod_dict = {
                'id': product.id,
                'name': product.name,
                'box_art': product.box_art,
                'price': stock.price,
                'in_stock': stock.in_stock,
                'platforms': stock.platforms,
                'update_form': UpdateShopProductForm(),
            }

            prod_dict['update_form']['price'].initial = stock.price
            prod_dict['update_form']['in_stock'].initial = stock.in_stock
            prod_dict['update_form']['platforms'].initial = stock.platforms.split(
                ', ')
            context['products'].append(prod_dict)

    except Exception as e:
        print("ERROR! ", e)
        messages.warning(request, "Internal server error")
        return HttpResponseRedirect(reverse("products:featured_products"))

    return render(request, 'user_profile/my_products.html', context)


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['shop'])
def new_products(request):
    context = {'products': []}

    try:
        shop = Shop.objects.get(email=request.user)
        context['shop_name'] = shop.shop_name

        if request.method == 'POST':
            if 'add' in request.POST:
                form = AddNewProductForm(request.POST)

                if form.is_valid():
                    # print(request.POST)

                    product_id = request.POST.get('add')
                    product = Product.objects.get(id=product_id)

                    Stock.objects.create(
                        shop=shop,
                        product=product,
                        price=form.cleaned_data.get('price'),
                        in_stock=form.cleaned_data.get('in_stock'),
                        platforms=', '.join(
                            form.cleaned_data.get('platforms')),
                    )

                    return HttpResponseRedirect(reverse("user_profile:new_products"))

        products = Product.objects.raw(
            'SELECT * FROM products_product WHERE products_product.id NOT IN (SELECT\
            product_id FROM products_stock WHERE shop_id = {})'.format(shop.id))

        for product in products:
            context['products'].append({
                'id': product.id,
                'name': product.name,
                'box_art': product.box_art,
                'form': AddNewProductForm(),
            })

    except Exception as e:
        print(e)
        messages.error(request, 'Server error')
        return HttpResponseRedirect(reverse("products:featured_products"))

    return render(request, 'user_profile/new_products.html', context)


def user_profile_home(request):
    return HttpResponseRedirect(reverse('products:featured_products'))

    # print(shop.id)
    # print(product_ids)

    # my_product_ids = get_product_ids(shop.id, False)
    # product_ids =
    # context['products'] = []
    # for id in my_product_ids:
    #     context['products'].append(
    #         get_product_dict(shop.id, id, False))

    # new_product_ids = get_product_ids(shop.id, True)
    # context['products'] = []
    # for id in new_product_ids:
    #     context['products'].append(
    #         get_product_dict(shop.id, id, True))

    #         elif 'cancel_add_product' in request.POST:
    #             return HttpResponseRedirect(reverse("user_profile:new_products"))

    #     elif request.method == 'GET':
    #         if 'add_to_store' in request.GET:
    #             product_id = request.GET.get('add_to_store')

    #             form = AddNewProductForm()
    #             form.box_art = Product.objects.get(id=product_id).box_art
    #             form.id = product_id

    #             context['add_product_form'] = form

# def get_product_ids(shop_id, get_new):
#     shop_product_ids = Stock.objects.filter(
#         shop=shop_id).values_list('product', flat=True)

#     if get_new == False:
#         return shop_product_ids

#     sellable_product_ids = Product.objects.filter(
#         can_sell=True).values_list('id', flat=True)

#     return [id for id in sellable_product_ids if id not in shop_product_ids]

# def get_my_products(shop_id):
#     product_ids = Stock.objects.filter(
#         shop=shop_id).values_list('product', flat=True)

#     return product_ids


# def get_product_dict(shop_id, product_id, get_new):
#     product = Product.objects.get(id=product_id)

#     if get_new == False:
#         stock = Stock.objects.get(shop=shop_id, product=product_id)
#         prod_dict = {
#             'id': product_id,
#             'name': product.name,
#             'box_art': product.box_art,
#             'price': stock.price,
#             'in_stock': stock.in_stock,
#             'platforms': stock.platforms,
#             'update_form': UpdateShopProductForm(),
#         }

#         prod_dict['update_form']['price'].initial = stock.price
#         prod_dict['update_form']['in_stock'].initial = stock.in_stock
#         prod_dict['update_form']['platforms'].initial = stock.platforms.split(
#             ', ')

#         return prod_dict

#     add_product_form = AddNewProductForm()
#     add_product_form.id = product.id
#     # add_product_form.fields['platforms'].required = True

#     return {'name': product.name, 'box_art': product.box_art, 'form': add_product_form}
