from .models import Movie, CriticUser, Rating
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')



class loginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password')



class RatingForm(forms.ModelForm):
	class Meta:
		model = Rating
		fields = ('rating',)