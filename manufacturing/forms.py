from django import forms
from .models import OrdenProduccion

class OrdenProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenProduccion
        fields = ['coche', 'cantidad', 'estado']