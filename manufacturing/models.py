from django.db import models
from ecommerce.models import Producto

class OrdenProduccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('Planificada', 'Planificada'), ('En Progreso', 'En Progreso'), ('Completada', 'Completada')], default='Planificada')

    def __str__(self):
        return f"Orden {self.id} - {self.producto.nombre}"