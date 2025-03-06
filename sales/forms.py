from django import forms
from .models import Pedido, PedidoItem

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'estado']

class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ['producto', 'cantidad']