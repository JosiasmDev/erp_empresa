# ecommerce/forms.py
from django import forms

class PasarelaPagoForm(forms.Form):
    nombre_completo = forms.CharField(max_length=100, label="Nombre completo")
    email = forms.EmailField(label="Correo electrónico")
    numero_tarjeta = forms.CharField(max_length=16, label="Número de tarjeta")
    fecha_expiracion = forms.CharField(max_length=5, label="Fecha de expiración (MM/AA)")
    cvv = forms.CharField(max_length=4, label="CVV")
    aceptar_contrato = forms.BooleanField(label="Acepto el contrato de compra-venta")