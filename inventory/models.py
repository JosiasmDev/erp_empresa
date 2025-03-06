from django.db import models
from ecommerce.models import Producto
from django.utils import timezone

class MovimientoStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')])
    fecha = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.tipo == 'Entrada':
            self.producto.stock += self.cantidad
        elif self.tipo == 'Salida':
            self.producto.stock -= self.cantidad
        self.producto.save()

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre}"