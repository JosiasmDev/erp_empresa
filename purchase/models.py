# purchase/models.py
from django.db import models
from ecommerce.models import Coche
from crm.models import Cliente
from manufacturing.models import Componente

class Compra(models.Model):
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name="compras"
    )
    coche = models.ForeignKey(
        Coche, 
        on_delete=models.CASCADE, 
        related_name="compras"
    )
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ["-fecha"]

    def marcar_como_pagada(self):
        """Marca la compra como pagada y la guarda en la base de datos."""
        self.pagado = True
        self.save()

    def __str__(self):
        return f"Compra {self.id} - Cliente: {self.cliente.nombre} - Coche: {self.coche.nombre} - {'Pagado' if self.pagado else 'Pendiente'}"

class OrdenCompra(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en_transito', 'En Tránsito'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero_orden = models.CharField(max_length=20, unique=True)
    fecha_orden = models.DateTimeField(auto_now_add=True)
    fecha_entrega_esperada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Orden Compra {self.numero_orden}"
    
    def save(self, *args, **kwargs):
        if not self.numero_orden:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero_orden = f"OC-{timestamp}"
        super().save(*args, **kwargs)

class DetalleOrdenCompra(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.orden.numero_orden} - {self.componente.nombre}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Actualizar el total de la orden
        self.orden.total = sum(detalle.subtotal for detalle in self.orden.detalleordencompra_set.all())
        self.orden.save()