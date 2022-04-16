from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    #https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'first name',
            'id': 'firstnameInput'}
    ))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'last name',
            'id': 'lastnameInput'}
    ))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'email address',
            'id': 'emailInput'}
    ))
    username = UsernameField(widget=forms.TextInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'username',
            'id': 'usernameInput'}
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'password',
            'id': 'password1Input'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'confirm password',
            'id': 'password2Input'
        }
    ))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'username',
            'id': 'usernameInput'}
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'password',
            'id': 'passwordInput'
        }
    ))

    