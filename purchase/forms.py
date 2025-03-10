from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['cliente', 'coche', 'precio_total']

    def clean_precio_total(self):
        precio_total = self.cleaned_data['precio_total']
        if precio_total < 0:
            raise forms.ValidationError("El precio total no puede ser negativo.")
        return precio_total