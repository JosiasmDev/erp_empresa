from django import forms
from .models import Coche

class CocheConfigForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = ['nombre', 'tamanio', 'precio_base', 'potencia', 'velocidad_maxima', 'descripcion', 'color', 'rueda']