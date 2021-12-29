from django.urls import reverse
from django.contrib import messages
from django.http.response import HttpResponseRedirect


from order.models import Order, OrderItem
from user_profile.models import Profile
from users.models import Customer, NewUser
from product.models import Product


def extras(request):
    # pass
    context = {}

    try:
        context['featured_products'] = []

        for product in Product.objects.raw(
                "select * from product_product where ingredients != '' order by random() limit 12"):
            context['featured_products'].append(
                {
                    'id': product.id,
                    'name': product.name,
                    'image': product.image,
                    'price': product.price,
                }
            )
        
        # context['featured_products'][0] = Product.objects.get(pk=31)

        cart_count = 0

        if request.user.is_authenticated and request.user.groups.all()[0].name == 'customer':
            context['username'] = Profile.objects.get(user=NewUser.objects.get(email=request.user)).username
            order, created = Order.objects.get_or_create(user=request.user, status='incomplete')
            cart_count = OrderItem.objects.filter(order=order).count()

        context['cart_count'] = cart_count
        
    except Exception as e:
        messages.warning(request, 'Internal server error.')
        print("Exception in custom context processor")
        return HttpResponseRedirect(reverse('home:home'))

    return context
