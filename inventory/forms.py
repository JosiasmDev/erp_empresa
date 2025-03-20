from django import forms
from .models import MovimientoStock, Stock

class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['componente', 'tipo', 'cantidad']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stock_minimo', 'stock_maximo', 'ubicacion', 'notas']
        widgets = {
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }