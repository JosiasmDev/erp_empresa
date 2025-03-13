from django import forms
from .models import Campana
from website.models import Coche, PersonalizacionComponente

class CampanaForm(forms.ModelForm):
    class Meta:
        model = Campana
        fields = ['nombre', 'objetivo', 'fecha_envio', 'estado']

class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = ['nombre', 'descripcion', 'precio_base']

class PersonalizacionComponenteForm(forms.ModelForm):
    class Meta:
        model = PersonalizacionComponente
        fields = ['nombre', 'opcion', 'precio_adicional']