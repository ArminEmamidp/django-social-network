from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile, Story, Music


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Enter password', 'class':'form-control'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'placeholder':'Enter password', 'class':'form-control'}))
    

class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Enter password', 'class':'form-control'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'Enter email', 'class':'form-control'}))
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Enter first-name', 'class':'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Enter last-name', 'class':'form-control'}))
    password1 = forms.CharField(label='Password', max_length=200, widget=forms.PasswordInput(attrs={'placeholder':'Enter password', 'class':'form-control'}))
    password2 = forms.CharField(label='Confirm password', max_length=200, widget=forms.PasswordInput(attrs={'placeholder':'Enter password', 'class':'form-control'}))
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        
        if user.exists():
            raise ValidationError('This username already exists')
        return username
    
    def clean(self):
        cd = self.cleaned_data
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords must match')


class UserEditProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'Enter email', 'class':'form-control'}))
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Enter first-name', 'class':'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Enter last-name', 'class':'form-control'}))

    class Meta:
        model = Profile
        fields = ['age', 'address', 'bio']
        widgets = {
            'address' : forms.TextInput(attrs={'placeholder':'Enter address', 'class':'form-control'}),
            'bio' : forms.Textarea(attrs={'placeholder':'Enter bio', 'class':'form-control'})
        }


class UserCreateStoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['body']
        widgets = {
            'body' : forms.Textarea(attrs={'placeholder':'Enter body', 'class':'form-control'})
        }


class UserCreateMusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['singer_name', 'song_name', 'music']
        widgets = {
            'singer_name' : forms.TextInput(attrs={'placeholder':'Enter singer-name', 'class':'form-control'}),
            'song_name' : forms.TextInput(attrs={'placeholder':'Enter song-name', 'class':'form-control'})            
        }