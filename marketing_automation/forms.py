from django import forms
from .models import Campana

class CampanaForm(forms.ModelForm):
    class Meta:
        model = Campana
        fields = ['nombre', 'objetivo', 'fecha_envio', 'estado']