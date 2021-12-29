from django.forms import ModelForm
from django import forms
from .models import Booking

PLATFORMS_CHOICES = [
    ('PS4', 'PS4'),
    ('PS5', 'PS5'),
    ('X Box One', 'X Box One',),
    ('X Box One X', 'X Box One X'),
    ('X Box One Series X', 'X Box One Series X'),
    ('Nintendo Switch', 'Nintendo Switch'),
    ('PC', 'PC'),
]


class NewBookingForm(ModelForm):
    product_name = ""
    shop_name = ""
    box_art = ""
    price = 0
    platforms = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PLATFORMS_CHOICES)

    class Meta:
        model = Booking
        fields = ('platforms',)
