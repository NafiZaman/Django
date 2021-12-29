from django import forms
from .models import Profile
from django.template.defaultfilters import mark_safe


class ProfileForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=50, label=mark_safe('<strong>Username</strong>'))
    phone_number = forms.CharField(required=True, label=mark_safe('<strong>Phone number</strong>'))
    date_of_birth = forms.DateField(required=False, label=mark_safe('<strong>Date of birth (yyyy-mm-dd)</strong>'))
    address = forms.CharField(max_length="250", required=False, label=mark_safe('<strong>Address</strong>'))
    post_code = forms.NumberInput()

    class Meta:
        model = Profile
        fields = ('username', 'phone_number', 'date_of_birth', 'address', 'post_code')

# class PostForm(forms.ModelForm):
#     # content = forms.Textarea(label='', widget=forms.Textarea(attrs={'placeholder': 'Food for thought?'}))

#     class Meta:
#         model = Post
#         fields = ('content',)
#         widgets = {
#             'content': forms.Textarea(attrs={'placeholder': 'Food for thought.....', 'style':'resize:none;'}),
#         }
#         labels = {
#             "content": ""
#         }