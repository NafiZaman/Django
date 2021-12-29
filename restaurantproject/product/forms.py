from django import forms
# from django.forms import fields
from .models import ProductReview
# from django.core.validators import MinValueValidator, MaxValueValidator


class ProductReviewForm(forms.ModelForm):
    # product_rating = forms.IntegerField(initial=0, required=True)
    review = forms.Textarea()

    class Meta:
        model = ProductReview
        fields = ('review',)
        widgets = {
            'review': forms.Textarea(attrs={
                'class':"form-control", 
                'id':"textAreaExample",
                'rows':"4",
                'style':"resize:none;",
                'placeholder':"Write a review...."}),
        }
        labels = {
            "review": ""
        }

    def clean_review(self, *args, **kwargs):
        review = self.cleaned_data.get('review')

        if review == '':
            raise forms.ValidationError("Cannot leave this field empty")

        return review
    # def clean_product_rating(self, *args, **kwargs):
    #     product_rating = self.cleaned_data.get('product_rating')

    #     if product_rating < 0 or product_rating > 5:
    #         raise forms.ValidationError("Pick a number between 0 and 5")
    #     return product_rating
