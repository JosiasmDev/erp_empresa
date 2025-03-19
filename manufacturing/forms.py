from django import forms
from .models import OrdenFabricacion, ComponenteOrden

class OrdenFabricacionForm(forms.ModelForm):
    class Meta:
        model = OrdenFabricacion
        fields = ['pedido', 'coche']

class ComponenteOrdenForm(forms.ModelForm):
    class Meta:
        model = ComponenteOrden
        fields = ['componente', 'cantidad', 'es_extra']