from django.db import models
from ecommerce.models import Coche
from crm.models import Cliente

class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False)
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE, null=False)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Compra {self.id} - {self.cliente.nombre}"