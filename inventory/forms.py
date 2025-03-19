from django import forms
from .models import MovimientoStock, Stock

class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['componente', 'cantidad', 'tipo']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        tipo = cleaned_data.get('tipo')
        componente = cleaned_data.get('componente')

        if cantidad and tipo and componente:
            stock, _ = Stock.objects.get_or_create(componente=componente)
            if tipo == 'salida' and cantidad > stock.cantidad:
                raise forms.ValidationError(f"No hay suficiente stock disponible. Stock actual: {stock.cantidad}")

        return cleaned_data

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['cantidad', 'stock_minimo', 'stock_maximo', 'ubicacion', 'notas']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 0}),
            'stock_minimo': forms.NumberInput(attrs={'min': 0}),
            'stock_maximo': forms.NumberInput(attrs={'min': 0}),
        }