from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Music, Profile


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
    password = forms.CharField(max_length=168, label='Password', widget=forms.TextInput(attrs={'placeholder':'Password', 'type':'password', 'class':'form-control'}))


class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'form-control'}))
    password1 = forms.CharField(max_length=168, label='Password', widget=forms.TextInput(attrs={'placeholder':'Password', 'type':'password', 'class':'form-control'}))
    password2 = forms.CharField(max_length=168, label='Password(Again)', widget=forms.TextInput(attrs={'placeholder':'Password', 'type':'password', 'class':'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)

        invalid_chars = ['<','>', '(',')', '[',']', '{','}', '.', ',', '/', '\\', '|', '=', '-', '`', '@', '#', '$', '%', '^', '*', '&', 'username']
        for char in invalid_chars:
            if char in username:
                raise ValidationError('Your username has invalid char(s)..!')

        if user.exists():
            raise ValidationError('This username already exists!')
        return username

    def clean(self):
        cd = self.cleaned_data
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords must match!')
        
        if len(p1) < 8 or len(p2) < 8:
            raise ValidationError('The Length of password(s) must be 8 or more character..!')
    

class UserUpdateProfileForm(forms.ModelForm):
    # username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'form-control'}))

    class Meta:
        model = Profile
        fields = ['address', 'bio', 'age']
        widgets = {
            'address' : forms.TextInput(attrs={'placeholder':'Address', 'class':'form-control'}),
            'bio' : forms.Textarea(attrs={'placeholder':'Bio', 'class':'form-control'}),
            'age' : forms.TextInput(attrs={'placeholder':'Age', 'type':'number', 'class':'form-control'})
        }


class UserMusicCreateForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['singer_name', 'music_name', 'music_file']
        widgets = {
            'singer_name' : forms.TextInput(attrs={'placeholder':'Singer-Name...', 'class':'form-control'}),
            'music_name' : forms.TextInput(attrs={'placeholder':'Music-Name...', 'class':'form-control'}),
            'music_file' : forms.FileInput(attrs={'class':'form-control-file'})
        }


class UserImageCreateForm(forms.Form):
    image_file = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))


class UserSearchForm(forms.Form):
    search_text = forms.CharField(label='', max_length=500, widget=forms.TextInput(attrs={'placeholder':'Search user...', 'class':'form-control'}))


class UserStoryCreateForm(forms.Form):
    content = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content...'}))


class UserLinkCreateForm(forms.Form):
    title = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title...'}))
    url = forms.URLField(label='', max_length=100, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Url...'}))
