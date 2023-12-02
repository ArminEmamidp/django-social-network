from django import forms 
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body' : forms.Textarea(attrs={'placeholder':'Add your text....', 'class':'form-control'})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body' : forms.Textarea(attrs={'placeholder':'Add your text....', 'class':'form-control'})
        }


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'main_image', 'description', 'body']
        widgets ={
            'title' : forms.TextInput(attrs={'placeholder':'Enter title', 'class':'form-control'}),
            'description' : forms.Textarea(attrs={'placeholder':'Enter description', 'class':'form-control'}),
            'body' : forms.Textarea(attrs={'placeholder':'Enter body', 'class':'form-control'}),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'main_image', 'description', 'body']
        widgets ={
            'title' : forms.TextInput(attrs={'placeholder':'Enter title', 'class':'form-control'}),
            'description' : forms.Textarea(attrs={'placeholder':'Enter description', 'class':'form-control'}),
            'body' : forms.Textarea(attrs={'placeholder':'Enter body', 'class':'form-control'}),
        }