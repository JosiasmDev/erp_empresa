from django.db import models
from sales.models import Pedido

class Factura(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=20, unique=True, null=True, blank=True)  # Añadir este campo
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateTimeField(auto_now_add=True)  # Cambiar fecha a fecha_emision
    pagada = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.id} - Pedido {self.pedido.id}"