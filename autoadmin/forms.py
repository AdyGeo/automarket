
from django import forms
from .models import ImaginiAuto

class ImaginiAutoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bulk_foto_upload'] = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta:
        model = ImaginiAuto
        fields = ['autovehicul']