from django.db import models
from ecommerce.models import Producto

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    proveedor = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)