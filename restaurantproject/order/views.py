from django.db.models import F, Q
from django.contrib import messages
from django.db.models.aggregates import Sum
from django.urls.base import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, JsonResponse
import datetime

from .models import *
# from users.models import Customer
from product.models import Product, Stock
from users.decorators import ajax_allowed_users, ajax_login_required, allowed_users


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['customer'])
def view_cart(request):
    context = {}

    try:
        order = Order.objects.get(user=request.user, status="incomplete")
        context['order_id'] = order.id

        if request.method == 'POST':
            OrderItem.objects.filter(pk=request.POST.get('remove'), order=order).delete()    

        order_items = OrderItem.objects.filter(order=order, order__status = "incomplete").order_by('-date_added')

        context['order_items'] = []
        for item in order_items:
            context['order_items'].append(
                {   
                    'id': item.id,
                    'image': item.product.image,
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'max_quantity': Stock.objects.get(product=item.product).quantity,
                    'total_price': item.total_price,
                    'date_added': item.date_added,
                }
            )

        context['total_cost'] = OrderItem.objects.filter(order=order, order__status = "incomplete").aggregate(Sum('total_price'))['total_price__sum']

    except Exception as e:
        print("Error", e)
        messages.error(request, 'Server error')
        return HttpResponseRedirect(reverse('home:home'))

    return render(request, 'order/cart.html', context)

@ajax_login_required
@ajax_allowed_users(allowed_roles=['customer'])
def update_cart(request):
    context = {}

    try:
        if request.is_ajax and request.method == 'POST':
            # print(request.POST)
            order_id = int(request.POST.get('order_id'))
            item_id = int(request.POST.get('item_id'))
            quantity = int(request.POST.get('quantity'))

            item = OrderItem.objects.get(pk=item_id, order=order_id)      
            item.quantity = quantity
            item.total_price = quantity * item.product.price
            item.save()

            context['new_total_price'] = item.total_price
            context['total_cost'] = OrderItem.objects.filter(order=order_id, order__status="incomplete").aggregate(Sum('total_price'))['total_price__sum']

    except Exception as e:
        print("Error in update cart:", e)
        messages.error(request, 'Server error')
        context['server_error'] = True

    return JsonResponse(context)

@ajax_login_required
@ajax_allowed_users(allowed_roles=['customer'])
def add_to_cart(request):
    context = {}

    try:
        if request.is_ajax and request.method == 'POST':
            print(request.POST)
            product_id = int(request.POST.get('product_id'))
            quantity = int(request.POST.get('quantity'))

            product = Product.objects.get(pk=product_id)
            stock = Stock.objects.get(product=product)

            if quantity <= stock.quantity:
                order, created = Order.objects.get_or_create(user=request.user, status="incomplete")
                orderItem, created = OrderItem.objects.get_or_create(
                    product = product,
                    order = order,
                )
                
                orderItem.quantity = quantity
                orderItem.total_price = product.price * quantity
                orderItem.save()
                
                cart_count = OrderItem.objects.filter(order=order, order__status = "incomplete").count()
                context['cart_count'] = cart_count
            else:
                context['not_in_stock'] = True

    except Exception as e:
        messages.error(request, 'Server error')
        print("Error occured", e)
        context['server_error'] = True

    return JsonResponse(context)

@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['customer'])
def checkout(request):
    context = {}

    try:
        if request.method == 'POST':
            order_items = OrderItem.objects.filter(order__user = request.user, order__status = "incomplete")

            if 'checkout' in request.POST:
                
                context['order_id'] = order_items[0].order_id
                context['order_items'] = []
                
                for item in order_items:
                    name = item.product.name
                    image = item.product.image

                    item_stock_quantity = Stock.objects.get(product=item.product).quantity 

                    if item_stock_quantity == 0:
                        quantity="Out of stock"
                        total_price=0
                        OrderItem.objects.get(pk=item.id).delete()
                    elif item.quantity > item_stock_quantity:
                        item.quantity = item_stock_quantity
                        item.total_price = item_stock_quantity * item.product.price
                        item.save()
                        quantity = str(item.quantity)
                        total_price = item.total_price
                    else:
                        quantity = str(item.quantity)
                        total_price = item.total_price

                    context['order_items'].append(
                        {
                            'name':name,
                            'image':image,
                            'quantity':quantity,
                            'total_price':total_price,
                        }
                    )
                
                context['total_cost'] = order_items.aggregate(Sum('total_price'))['total_price__sum']


            elif 'confirm' in request.POST:
                for item in order_items:
                    stock = Stock.objects.get(product=item.product)
                    # print(stock)
                    stock.quantity = F('quantity') - item.quantity
                    stock.save()
                    # break

                order = Order.objects.get(pk=order_items[0].order_id)
                order.status = "confirmed"
                order.order_date = datetime.datetime.now()
                order.save()

                return HttpResponseRedirect(reverse('order:my_orders'))

    except Exception as e:
        print("Error in checkout:", e)
        messages.error(request, 'Server error')
        return HttpResponseRedirect(reverse('home:home'))
    
    return render(request, 'order/order_confirmation.html', context)

    

@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['customer'])
def my_orders(request):
    context = {}

    try:
        orders = Order.objects.filter(Q(user_id=request.user), (Q(status='complete') | Q(status='confirmed'))).order_by('-order_date')
        
        context['orders'] = {}

        for order in orders:
            context['orders'][order.id] = {'order_id':order.id,'date_confirmed':order.order_date, 'order_items':[], 'total_cost':0, 'status': order.status}

            for order_item in OrderItem.objects.filter(order_id=order.id):
                context['orders'][order.id]['order_items'].append(
                    {
                        'name':order_item.product.name,
                        'image':order_item.product.image,
                        'quantity':order_item.quantity,
                        'total_price':order_item.total_price,
                        'date_added':order_item.date_added,
                    }
                )
            
            context['orders'][order.id]['total_cost'] = OrderItem.objects.filter(order_id=order.id).aggregate(Sum('total_price'))['total_price__sum']

        # print(context['orders'][16]['order_items'])
        # print(context)
    except Exception as e:
        print("Error in my_orders:", e)
        messages.error(request, 'Server error')
        return HttpResponseRedirect(reverse('home:home'))

    return render(request, 'order/my_orders.html', context)