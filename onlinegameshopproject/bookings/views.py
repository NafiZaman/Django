from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect


from users.decorators import allowed_users
from products.models import Stock
from .forms import NewBookingForm
from bookings.models import Booking
from users.models import Customer, Shop
from django.contrib import messages


# def get_user_bookings(is_shop, user):
#     if is_shop:
#         bookings =


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['customer'])
def new_booking(request, stock_id):
    context = {}

    try:
        stock = Stock.objects.get(id=stock_id, in_stock=True)

        if request.method == 'GET':

            form = NewBookingForm()
            form.stock_id = stock.id
            form.product_name = stock.product.name
            form.shop_name = stock.shop.shop_name
            form.box_art = stock.product.box_art
            form.price = stock.price
            form.fields['platforms'].choices = [
                (plt, plt) for plt in stock.platforms.split(', ')]
            # form.fields['quantity'] = forms.IntegerField(initial=1,
            #                                              max_value=stock.quantity,
            #                                              min_value=1,
            #                                              label="How many do you want?")

            context['form'] = form

        elif request.method == 'POST':
            form = NewBookingForm(request.POST)

            if form.is_valid():
                # print(request.POST)
                # stock.quantity = F('quantity') - \
                #     form.cleaned_data.get('quantity')
                # stock.save()
                # print(stock.quantity)

                Booking.objects.create(
                    stock=Stock.objects.get(id=stock_id),
                    customer=Customer.objects.get(email=request.user),
                    platform=form.cleaned_data.get('platforms'),
                )
                return HttpResponseRedirect(reverse('products:featured_products'))

    except Exception as e:
        print("ERROR! ", e)
        return HttpResponseRedirect(reverse('products:featured_products'))

    return render(request, 'bookings/new_booking.html', context)


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['shop'])
def shop_bookings(request):
    context = {'shop_name': ""}

    try:
        shop = Shop.objects.get(email=request.user)
        context['shop_name'] = shop.shop_name

        if request.method == 'POST':
            booking_id = request.POST.get('booking')
            booking = Booking.objects.get(id=booking_id)
            # print(request.POST)

            if 'arrived' in request.POST:
                booking.is_arrived = True
            else:
                booking.is_arrived = False

            if 'pickedup' in request.POST:
                booking.is_picked_up = True
            else:
                booking.is_picked_up = False

            booking.save()
            return HttpResponseRedirect(reverse('bookings:shop_bookings'))

        bookings = Booking.objects.filter(stock__shop=shop)

        context['bookings'] = []
        for booking in bookings:
            context['bookings'].append({
                'id': booking.id,
                'customer': booking.customer.username,
                'product_name': booking.stock.product.name,
                'platform': booking.platform,
                'price': booking.stock.price,
                'is_arrived': booking.is_arrived,
                'is_picked_up': booking.is_picked_up,
                'booking_date': booking.date_added,
            })

    except Exception as e:
        print("ERROR! ", e)
        messages.error(request, 'Server error')
        return HttpResponseRedirect(reverse('products:featured_products'))
        # return HttpResponseRedirect(reverse('home:home'))

    return render(request, 'bookings/shop_bookings.html', context)


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['customer'])
def customer_bookings(request):
    context = {'username': ""}

    try:
        customer = Customer.objects.get(email=request.user)
        context['username'] = customer.username

        if request.method == 'POST':
            booking_id = request.POST.get('cancel')
            booking = Booking.objects.get(id=booking_id)

            if booking.customer == customer:
                # print("This is valid")
                booking.delete()
                return HttpResponseRedirect(reverse('bookings:customer_bookings'))

        bookings = Booking.objects.filter(
            customer=customer, is_picked_up=False, stock__isnull=False)

        context['bookings'] = []

        for booking in bookings:
            context['bookings'].append({
                'id': booking.id,
                'product_name': booking.stock.product.name,
                'shop': booking.stock.shop.shop_name,
                'platform': booking.platform,
                'price': booking.stock.price,
                'is_arrived': booking.is_arrived,
                'booking_date': booking.date_added,
            })

    except Exception as e:
        print("ERROR! ", e)
        messages.error(request, 'Server error')
        return HttpResponseRedirect(reverse('products:featured_products'))

    return render(request, 'bookings/customer_bookings.html', context)
