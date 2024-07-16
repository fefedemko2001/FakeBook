from django import forms
from django.forms.models import inlineformset_factory
from .models import Post, Image

class ImageForm(forms.ModelForm):
    delete = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Image
        fields = ['image', 'description', 'delete']

ImageFormSet = inlineformset_factory(Post, Image, fields=['image', 'description'], extra=0)

