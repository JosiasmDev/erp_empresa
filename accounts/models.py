from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = (
        ('administrador', 'Administrador'),
        ('gerente', 'Gerente'),
        ('finanzas', 'Finanzas'),
        ('produccion', 'Producción'),
        ('recursos_humanos', 'Recursos Humanos'),
        ('marketing', 'Marketing'),
        ('cliente', 'Cliente'),  # Nuevo rol agregado
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='administrador')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def get_permissions(self):
        permissions = {
            'administrador': ['*'],
            'gerente': ['*'],
            'finanzas': ['accounting', 'crm', 'sales', 'purchase'],
            'produccion': ['manufacturing', 'inventory'],
            'recursos_humanos': ['human_resources', 'create_employee'],
            'marketing': ['marketing_automation', 'ecommerce'],
            'cliente': ['website', 'home'],  # Solo acceso a Website y Home
        }
        return permissions.get(self.role, [])