from django.forms import ModelForm
from django import forms
from .models import Post, Comment, Reply

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body', 'tags']
        labels = {
            'body': 'Caption',
            'tags': 'Category',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption...', 'class': 'font1 text-4xl'}),
            'url': forms.TextInput(attrs={'placeholder': 'Add url ...'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'tags']
        labels = {
            'body': '',
            'tags': 'Category',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'class': 'font1 text-4xl'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            # 'body': forms.TextInput(attrs={'placeholder': 'Add comment ...', 'style': 'width: 530px; height: 55px;'})
            'body': forms.TextInput(attrs={
                'placeholder': 'Add comment ...',
                'class': 'w-full p-3 border rounded-md'
            })
        }           


class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            # 'body': forms.TextInput(attrs={'placeholder': 'Add comment ...', 'class': '!text-sm'})
            'body': forms.TextInput(attrs={
                'placeholder': 'Add reply ...',
                'class': 'w-full p-3 border rounded-md !text-sm'
            })            
        }           