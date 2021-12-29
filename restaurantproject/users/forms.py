from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields

from users.models import Customer


class CustomerForm(UserCreationForm):

    class Meta:
        model = Customer
        fields = ('email', 'password1', 'password2', 'phone_number')
