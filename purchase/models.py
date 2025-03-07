from django.db import models
from inventory.models import Pieza

class Compra(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    proveedor = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra {self.id} - {self.pieza.nombre}"