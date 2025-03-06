from django import forms
from .models import Pagina

class PaginaForm(forms.ModelForm):
    class Meta:
        model = Pagina
        fields = ['titulo', 'contenido', 'publicada']