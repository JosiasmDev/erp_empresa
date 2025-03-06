from django.db import models
from ecommerce.models import Producto

class MovimientoStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo = models.CharField(max_length=10)  # Entrada/Salida