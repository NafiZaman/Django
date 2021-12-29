from django import forms
from django.core.exceptions import ValidationError
from .models import *

class ProfileForm(forms.ModelForm):
    pic = forms.ImageField(required=False, label="Profile Picture")
    rel_status = forms.ChoiceField(choices=[
        ('single', 'single'),
        ('engaged', 'engaged'),
        ('married', 'married'),
    ], widget=forms.RadioSelect, required=False)

    class Meta:
        model = Profile
        fields = ('pic', 'bio', 'work', 'education', 'location', 'rel_status')
        exclude = ['user','profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class':'mt-2',
                'rows':'2',
                'style':"resize:none;",
                'placeholder':"Write something about yourself....."
            }),
        }
        # labels = {
        #     "pic":"Profile Picture",
        # }

    def clean_pic(self, *args, **kwargs):
        pic = self.cleaned_data.get('pic', False)
        if pic:
            if (pic.size / 1000) > 1024:
                raise forms.ValidationError("Image file cannot be more than 1MB")
        return pic
            