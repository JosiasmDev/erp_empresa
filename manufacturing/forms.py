from django import forms
from .models import OrdenFabricacion, ComponenteOrden
from ecommerce.models import Coche, Pedido

class OrdenFabricacionForm(forms.ModelForm):
    class Meta:
        model = OrdenFabricacion
        fields = ['pedido', 'coche']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo los pedidos pendientes
        self.fields['pedido'].queryset = Pedido.objects.filter(estado='pendiente')
        # Filtrar solo los coches disponibles
        self.fields['coche'].queryset = Coche.objects.filter(disponible=True)

class ComponenteOrdenForm(forms.ModelForm):
    class Meta:
        model = ComponenteOrden
        fields = ['componente', 'cantidad', 'es_extra']