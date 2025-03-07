from django.db import models
from ecommerce.models import Coche

class Pieza(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_disponible = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class MovimientoStock(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')])
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.tipo == 'Entrada':
            self.pieza.cantidad_disponible += self.cantidad
        elif self.tipo == 'Salida':
            self.pieza.cantidad_disponible -= self.cantidad
        self.pieza.save()

    def __str__(self):
        return f"{self.tipo} - {self.pieza.nombre}"