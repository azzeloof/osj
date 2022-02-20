from django import forms
from things.models import Thing, Image, File, Category, Licence
from tinymce.widgets import TinyMCE
import taggit
from tagify.fields import TagField
from tagify.widgets import TagInput


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


def getTags():
    tags = taggit.models.Tag.objects.all()
    options = []
    for tag in tags:
        options.append(str(tag))
    return options

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
    description = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 80, 'rows': 20}
        )
    )
    tagline = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 80, 'rows': 10}
        )
    )
    repo = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control title-input'}
        )
    )
    tags = TagField(
        label='tags',
        place_holder='add a tag',
        delimiters=',',
        max_tags=10,
        data_list=getTags,
        widget=TagInput(
            attrs={'class': 'form-control'}
        )
    )
    class Meta:
        model = Thing
        fields = ['title', 'tagline', 'description', 'licence', 'repo', 'category', 'tags']


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
