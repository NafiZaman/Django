from django.forms import ModelForm
from django import forms
from .models import Stock

PLATFORMS_CHOICES = [
    ('PS4', 'PS4'),
    ('PS5', 'PS5'),
    ('X Box One', 'X Box One',),
    ('X Box One X', 'X Box One X'),
    ('X Box One Series X', 'X Box One Series X'),
    ('Nintendo Switch', 'Nintendo Switch'),
    ('PC', 'PC'),
]


class AddNewProductForm(ModelForm):
    # id = 0
    price = forms.IntegerField(min_value=0)
    # quantity = forms.IntegerField(min_value=0, label="How many in stock?")
    # box_art = ""
    platforms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=PLATFORMS_CHOICES)

    class Meta:
        model = Stock
        fields = ('price', 'platforms', 'in_stock',)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     selected = cleaned_data.get('selected')
    #     price = cleaned_data.get('price')

    #     if (selected == True and (price == None or price <= 0)) or (price > 0 and selected == False):
    #         raise ValidationError("Invalid")

    #     return cleaned_data


class UpdateShopProductForm(ModelForm):
    # id = 0
    product_name = ""
    price = forms.IntegerField(min_value=0)
    # quantity = forms.IntegerField(min_value=0, label="How many in stock?")
    # box_art = ""
    platforms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=PLATFORMS_CHOICES)

    class Meta:
        model = Stock
        fields = ('price', 'in_stock')
