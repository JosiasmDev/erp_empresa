from django import forms
from .models import Pedido, PedidoItem  # Añadimos PedidoItem a la importación

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'coche', 'color', 'rueda']

class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ['pedido', 'coche', 'cantidad']