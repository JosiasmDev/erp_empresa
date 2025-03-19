from django.db import models
from ecommerce.models import Coche
from manufacturing.models import Componente

class OrdenEntrega(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero_orden = models.CharField(max_length=20, unique=True)
    pedido = models.OneToOneField('ecommerce.Pedido', on_delete=models.CASCADE, related_name='orden_entrega_rel')
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    def __str__(self):
        return f"Orden Entrega {self.numero_orden}"

    def save(self, *args, **kwargs):
        if not self.numero_orden:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero_orden = f"OE-{timestamp}"
        super().save(*args, **kwargs)

class Stock(models.Model):
    componente = models.OneToOneField(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.componente.nombre} - Stock: {self.cantidad}"

class MovimientoStock(models.Model):
    TIPOS = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    ]
    
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPOS)
    fecha = models.DateTimeField(auto_now_add=True)
    orden_entrega = models.ForeignKey(OrdenEntrega, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.componente.nombre} - {self.cantidad}"