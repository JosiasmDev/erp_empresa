from django import forms
from .models import MovimientoStock, Stock

class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['componente', 'cantidad', 'tipo', 'descripcion']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 0}),
        }