from django import forms
from things.models import Thing, Image, File, Category
from tinymce.widgets import TinyMCE


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
    description = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 80, 'rows': 20}
        )
    )
    repo = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control title-input'}
        )
    )
    class Meta:
        model = Thing
        fields = ['title', 'description', 'repo', 'category']
        

class ThingImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'alt', 'featured']


class ThingFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file', 'default']


ThingImageFormset = forms.inlineformset_factory(Thing, Image, form=ThingImageForm, extra=1)
ThingFileFormset = forms.inlineformset_factory(Thing, File, form=ThingFileForm, extra=1)                                
