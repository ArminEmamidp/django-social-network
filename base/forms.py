from django import forms
from froala_editor.widgets import FroalaEditor


class PostCreateForm(forms.Form):
    title = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'placeholder':'Title', 'class':'form-control'}))
    # image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description', 'class':'form-control'}))
    # body = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Body', 'class':'form-control'}))
    body = forms.CharField(widget=FroalaEditor)


class CommentSendForm(forms.Form):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Comment...', 'class':'form-control', 'id':'user_text'}))


class PostSearchForm(forms.Form):
    search_text = forms.CharField(label='', max_length=500, widget=forms.TextInput(attrs={'placeholder':'Search post...', 'class':'form-control'}))
