from django import forms
from .models import Pedido, PedidoItem

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'coche', 'color', 'rueda', 'estado']

class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ['coche', 'cantidad']  # Cambiado de 'producto' a 'coche'