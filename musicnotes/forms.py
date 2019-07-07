from django.contrib.auth.models import User
from .models import Profile, Song, InstrumentPart
from django import forms


class SongForm(forms.ModelForm):
    title = forms.CharField(max_length=50, required=True)
    artist = forms.CharField(max_length=50, required=True)
    key = forms.CharField(max_length=3, required=True)

    class Meta:
        model = Song
        fields = ['title', 'artist', 'key']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(max_length=75, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class ProfileForm(forms.ModelForm):
    preference = forms.BooleanField(required=True)

    class Meta:
        model = Profile
        fields = ['preference']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class InstrumentForm(forms.ModelForm):
    capo = forms.IntegerField(required=False)
    music = forms.CharField(max_length=1000, required=False)

    class Meta:
        model = InstrumentPart
        fields = ['capo', 'music']