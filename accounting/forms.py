from django import forms
from .models import Cuenta

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['tipo', 'descripcion', 'monto', 'pedido', 'empleado', 'orden_compra']