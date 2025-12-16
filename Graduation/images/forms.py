from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['photo', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a description...'}),
        }
