from django import forms
from .models import OrdenProduccion

class OrdenProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenProduccion
        fields = ['coche', 'cantidad', 'completada']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['completada'].initial = False
        self.fields['completada'].widget.attrs['readonly'] = True  # Solo se actualiza por la lógica