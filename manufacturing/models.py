# manufacturing/models.py
from django.db import models
from django.utils import timezone
from datetime import datetime

class OrdenFabricacion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ]
    
    numero_orden = models.CharField(max_length=20, unique=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    pedido = models.OneToOneField('sales.Pedido', on_delete=models.SET_NULL, null=True, blank=True)
    coche = models.ForeignKey('ecommerce.Coche', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Componentes disponibles
    ruedas_disponibles = models.BooleanField(default=False)
    motorizacion_disponible = models.BooleanField(default=False)
    tapiceria_disponible = models.BooleanField(default=False)
    extras_disponibles = models.BooleanField(default=False)
    
    # Componentes asignados usando lazy loading
    ruedas_asignadas = models.ForeignKey('inventory.Componente', on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_ruedas')
    motorizacion_asignada = models.ForeignKey('inventory.Componente', on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_motor')
    tapiceria_asignada = models.ForeignKey('inventory.Componente', on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_tapiceria')
    extras_asignados = models.ForeignKey('inventory.Componente', on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_extras')
    
    def __str__(self):
        return f"Orden #{self.numero_orden} - {self.get_estado_display()}"
    
    def save(self, *args, **kwargs):
        if not self.numero_orden:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero_orden = f"OF-{timestamp}"
        super().save(*args, **kwargs)
    
    def verificar_componentes(self):
        return (self.ruedas_disponibles and 
                self.motorizacion_disponible and 
                self.tapiceria_disponible and 
                self.extras_disponibles)

class ComponenteOrden(models.Model):
    orden = models.ForeignKey(OrdenFabricacion, on_delete=models.CASCADE)
    componente = models.ForeignKey('inventory.Componente', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    es_extra = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.componente.nombre} - {self.orden.numero_orden}"