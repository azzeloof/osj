from cProfile import Profile
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from tinymce.widgets import TinyMCE
#import taggit
from django_bleach.forms import BleachField
from PIL import Image as pImage # Image conflicts with the model of the same name
from django.conf import settings


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class ProfilePhotoForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput())
    imageX = forms.FloatField(widget=forms.HiddenInput())
    imageY = forms.FloatField(widget=forms.HiddenInput())
    imageWidth = forms.FloatField(widget=forms.HiddenInput())
    imageHeight = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Profile
        fields = ['image', 'imageX', 'imageY', 'imageWidth', 'imageHeight']

    def save(self):
        profile = super(ProfilePhotoForm, self).save()
        x = self.cleaned_data.get('imageX')
        y = self.cleaned_data.get('imageY')
        w = self.cleaned_data.get('imageWidth')
        h = self.cleaned_data.get('imageHeight')
        image = pImage.open(profile.image)
        croppedImage = image.crop((x, y, x+w, y+h))
        resizedImage = croppedImage.resize((settings.PROFILE_PHOTO_SIZE), pImage.ANTIALIAS)
        resizedImage.save(profile.image.path)
        return profile
    

class ProfileDataForm(forms.ModelForm):
    description = BleachField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 80, 'rows': 20}
        )
    )
    class Meta:
        model = Profile
        fields = ['description']


class UserDataForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']