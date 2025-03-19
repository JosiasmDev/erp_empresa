from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Empleado(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('gerencia', 'Gerencia'),
        ('ventas', 'Ventas'),
        ('produccion', 'Producción'),
        ('rrhh', 'RRHH'),
        ('compras', 'Compras'),
        ('logistica', 'Logística'),
        ('contabilidad', 'Contabilidad'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, default='')
    cargo = models.CharField(max_length=50, choices=ROLES, default='ventas')
    sueldo_base = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_contratacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.get_cargo_display()}"

class Sueldo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Sueldo de {self.empleado.nombre} - {self.monto}€"