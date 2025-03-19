# purchase/models.py
from django.db import models
from django.utils import timezone
from manufacturing.models import Componente

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    fecha_registro = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('completada', 'Completada'),
    ]
    
    numero_orden = models.CharField(max_length=20, unique=True, default='')
    fecha = models.DateTimeField(default=timezone.now)
    fecha_entrega_esperada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Orden {self.numero_orden} - {self.proveedor.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.numero_orden:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero_orden = f"OC-{timestamp}"
        super().save(*args, **kwargs)

class DetalleOrdenCompra(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.componente.nombre} - {self.orden.numero_orden}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Actualizar el total de la orden
        self.orden.total = sum(detalle.subtotal for detalle in self.orden.detalles.all())
        self.orden.save()