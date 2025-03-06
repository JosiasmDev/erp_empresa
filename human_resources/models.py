from django.db import models
from django.utils import timezone

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_contratacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre