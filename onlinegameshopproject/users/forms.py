from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import NewUser


class CreateCustomerForm(UserCreationForm):
    username = forms.CharField()

    class Meta:
        model = NewUser
        fields = ('username', 'email', 'password1', 'password2')


class CreateShopForm(UserCreationForm):
    shop_name = forms.CharField()

    class Meta:
        model = NewUser
        fields = ('shop_name', 'email', 'password1', 'password2')
