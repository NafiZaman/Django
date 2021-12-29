# from django.contrib.auth.models import Group
from django.urls import reverse
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from . forms import CustomerForm
from . models import Customer
from . decorators import unauthenticated_user

@unauthenticated_user
def register(request):
    context = {}

    try:
        if request.method == 'POST':
            form = CustomerForm(request.POST)

            if form.is_valid():
                customer = Customer.objects.create(
                    email=form.cleaned_data.get('email'),
                    password=make_password(
                        form.cleaned_data.get('password1')),
                    phone_number=form.cleaned_data.get('phone_number')
                )

                # customer.groups.add(Group.objects.get(name='customer'))
                # customer.save()

                messages.success(request, "Account for " + customer.email + " was created successfully.")

                return HttpResponseRedirect(reverse('users:user_login'))

            context['form'] = form

        elif request.method == 'GET':
            form = CustomerForm()
            form.fields['phone_number'].initial = ""
            context['form'] = form

    except Exception as e:
        print(e)
        messages.error(request, 'Server Error. User could not be created')
        return HttpResponseRedirect(reverse('home:home'))

    return render(request, 'users/register.html', context)


@unauthenticated_user
@never_cache
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home:home'))
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'users/login.html')


@login_required(login_url='users:user_login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:home'))
