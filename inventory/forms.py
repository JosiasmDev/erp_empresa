from django import forms
from .models import MovimientoStock

class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['componente', 'cantidad', 'tipo', 'descripcion']