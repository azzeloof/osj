from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm, PasswordResetForm, PasswordChangeForm
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email address already exists!")
        return email

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


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'email',
            'id': 'emailInput'
        }
    ))
    
class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'old password',
            'id': 'oldPasswordInput'
        }
    ))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'new password',
            'id': 'newPassword1Input'
        }
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control title-input',
            'placeholder': 'confirm password',
            'id': 'newPassword2Input'
        }
    ))
    