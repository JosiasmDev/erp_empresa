from django import forms
from django.contrib.auth.models import User
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')

    class Meta:
        model = Empleado
        fields = ['nombre', 'cargo', 'sueldo_base', 'activo']
        widgets = {
            'sueldo_base': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'cargo': forms.Select(choices=Empleado.ROLES),
        }

    def save(self, commit=True):
        # Crear el usuario
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        
        # Crear el empleado
        empleado = super().save(commit=False)
        empleado.usuario = user
        if commit:
            empleado.save()
        return empleado