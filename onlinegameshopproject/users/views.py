from django.contrib.auth.models import Group
from django.urls import reverse
from django.shortcuts import render  # , get_object_or_404, render
from django.http.response import HttpResponseRedirect  # , HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from . models import Customer, Shop
# from django.contrib.auth import get_user_model
from . forms import CreateCustomerForm, CreateShopForm
from . decorators import unauthenticated_user  # , allowed_users


def home_page(request):
    return HttpResponseRedirect(reverse('products:featured_products'))


@unauthenticated_user
@never_cache
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('products:featured_products'))
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'users/login.html')


@login_required(login_url='users:user_login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('products:featured_products'))


@unauthenticated_user
def register(request, user_type):
    context = {'user_type': user_type}

    try:
        if request.method == 'POST':
            if user_type == 'shop':
                form = CreateShopForm(request.POST)

                if form.is_valid():
                    user = Shop.objects.create(
                        shop_name=form.cleaned_data.get('shop_name'),
                        email=form.cleaned_data.get('email'),
                        password=make_password(
                            form.cleaned_data.get('password1')),
                    )

                    user.groups.add(Group.objects.get(name='shop'))
                    user.save()

                    messages.success(request, "Account for " +
                                     form.cleaned_data.get('shop_name')+" successfully created")

                    return HttpResponseRedirect(reverse("users:user_login"))

            elif user_type == 'customer':
                if user_type == 'customer':
                    form = CreateCustomerForm(request.POST)

                    if form.is_valid():
                        user = Customer.objects.create(
                            username=form.cleaned_data.get('username'),
                            email=form.cleaned_data.get('email'),
                            password=make_password(
                                form.cleaned_data.get('password1')),
                        )

                        user.groups.add(Group.objects.get(name='customer'))
                        user.save()

                        messages.success(request, "Account for " +
                                         form.cleaned_data.get('username')+" successfully created")

                        return HttpResponseRedirect(reverse("users:user_login"))

            context['form'] = form

        elif user_type == 'shop':
            form = CreateShopForm()
            context['form'] = form

        elif user_type == 'customer':
            form = CreateCustomerForm()
            context['form'] = form

    except Exception as e:
        messages.error(request, 'Server error')
        return HttpResponseRedirect(reverse('products:featured_products'))

    return render(request, 'users/register.html', context)
