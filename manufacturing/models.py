from django.db import models
from ecommerce.models import Producto

class OrdenProduccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_inicio = models.DateTimeField(auto_now_add=True)