from django import forms
from .models import MovimientoStock

class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['pieza', 'cantidad', 'tipo']