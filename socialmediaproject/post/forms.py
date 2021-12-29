from django import forms
from django.forms import widgets
from .models import *

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text',)
        # exclude = ['user', 'post_image']
        widgets = {
            'text': forms.TextInput(attrs={
                # 'id': 'new-post-input',
                # 'class': 'mt-5',
                # 'rows': 1,
                # 'style': "resize:none;",
                # 'placeholder': 'Whats on your mind?'
                # 'type':'text',
                'class':'ms-2',
                # 'placeholder': "What's on your mind?" 
            })
        }
        labels = {
            "text":"",
        }

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('text',)
        # widgets = {
        #     'comment_text': forms.Textarea(attrs={
        #         'class': 'mt-3',
        #         # 'id': 'id_comment_text'
        #         'rows':1,
        #         'style':'resize:none;',
        #         'placeholder': 'Write a comment',
        #     })
        # }
        labels = {
            'text': "",
        }