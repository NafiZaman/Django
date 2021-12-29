# from django import forms
# # from django.db.models import fields
# from .models import *

# class UserUploadForm(forms.ModelForm):
#     # rel_status = forms.ChoiceField(choices=[
#     #     ('single', 'single'),
#     #     ('engaged', 'engaged'),
#     #     ('married', 'married'),
#     # ], widget=forms.RadioSelect, required=False)

#     class Meta:
#         model = UserUpload
#         fields = '__all__'
#         exclude = ['user',]
#         # widgets = {
#         #     'bio': forms.Textarea(attrs={
#         #         'class':'mt-2',
#         #         'rows':'2',
#         #         'style':"resize:none;",
#         #         'placeholder':"Write something about yourself....."
#         #     }),
#         # }
#         # labels = {
#         #     "profile_pic":"",
#         # }