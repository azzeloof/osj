from django import forms
from things.models import Thing, Image, File, Category, Licence
from tinymce.widgets import TinyMCE
#import taggit
from django_bleach.forms import BleachField

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class ThingForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control title-input',
                'size': 25,
                'style': 'font-size:24px;'
            }
        )
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    licence = forms.ModelChoiceField(queryset=Licence.objects.all())
    description = BleachField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 80, 'rows': 20}
        )
    )
    tagline = BleachField(
        widget=TinyMCEWidget(
            attrs={
                'required': False,
                'cols': 80,
                'rows': 10,
            },
            mce_attrs={}
        )
    )
    repo = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control title-input'}
        )
    )

    class Meta:
        model = Thing
        fields = ['title', 'tagline', 'description', 'licence', 'repo', 'category', 'tags']

    def __init__(self, *args, **kwargs):
        super(ThingForm, self).__init__(*args, **kwargs)
        self.fields['repo'].required = False


class ThingImageForm(forms.ModelForm):
    
    #alt = forms.CharField(required=False)
    #featured = forms.BooleanField(required=False)
    class Meta:
        model = Image
        fields = ['image', 'alt', 'featured', 'order']


class ThingFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file', 'default', 'order']


ThingImageFormset = forms.inlineformset_factory(Thing, Image, form=ThingImageForm, extra=1, can_order=True, can_delete=True)
ThingFileFormset = forms.inlineformset_factory(Thing, File, form=ThingFileForm, extra=1, can_order=True, can_delete=True)
