from django import forms
# from django.db.models import fields
# from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm

from .models import *

class NewUserForm(UserCreationForm):

    gender = forms.ChoiceField(choices=[
        ("male", "male"),
        ("female", "female"),
        ("other", "other"),
    ], widget=forms.RadioSelect(attrs={"style":'inline-block'}), label="")

    class Meta:
        model = NewUser
        fields = ('email', 'first_name', 'last_name', 'gender', 'dob', 'password1', 'password2',)
        widgets = {
            'dob': forms.DateInput(attrs={
                'type':"date",
            }),
        }
        labels = {
            "email": "",
            "first_name":"",
            "last_name": "",
            "dob": "",
            "password1":"",
            "password2":"",
        }

class UserSettingForm(forms.ModelForm):
    # post_visibility = forms.ChoiceField(choices=[
    #     ('public', 'public'),
    #     ('friends', 'friends'),
    #     ('private', 'private'),
    # ])

    class Meta:
        model = UserSetting
        fields = ('post_visibility', 'profile_visibility', 'upload_visibility',)
        labels={
            'post_visibility':"",
            'profile_visibility':"",
            'upload_visibility':"",
        }

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ('first_name', 'last_name', 'dob', 'gender',)
        # exclude = ('email', 'full_name',)


