# manufacturing/models.py
from django.db import models
from ecommerce.models import Coche

class OrdenFabricacion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero_orden = models.CharField(max_length=20, unique=True)
    pedido = models.OneToOneField('ecommerce.Pedido', on_delete=models.CASCADE, related_name='orden_fabricacion_rel')
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    def __str__(self):
        return f"Orden {self.numero_orden} - {self.coche.nombre}"

    def save(self, *args, **kwargs):
        if not self.numero_orden:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero_orden = f"OF-{timestamp}"
        super().save(*args, **kwargs)

class Componente(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    stock_minimo = models.IntegerField(default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre

class ComponenteOrden(models.Model):
    orden = models.ForeignKey(OrdenFabricacion, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    es_extra = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.componente.nombre} - {self.orden.numero_orden}"