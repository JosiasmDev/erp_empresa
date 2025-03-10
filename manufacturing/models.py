# manufacturing/models.py
from django.db import models
from ecommerce.models import Coche

class OrdenProduccion(models.Model):
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"Orden {self.id} - {self.coche.nombre}"