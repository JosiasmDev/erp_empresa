from django import forms
from ecommerce.models import Coche

class CocheConfigForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = ['color', 'rueda', 'motorizacion', 'tapiceria', 'extras']