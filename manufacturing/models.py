# manufacturing/models.py
from django.db import models
from ecommerce.models import Coche
from decimal import Decimal

class Componente(models.Model):
    TIPOS = [
        # Ruedas
        ('ruedas_17', 'Ruedas 17"'),
        ('ruedas_19', 'Ruedas 19"'),
        ('ruedas_21', 'Ruedas 21"'),
        # Motorizaciones
        ('motor_v6', 'Motor V6 3.0L'),
        ('motor_v8', 'Motor V8 4.0L'),
        ('motor_electrico', 'Motor Eléctrico 400kW'),
        # Tapicerías
        ('tapiceria_cuero_negro', 'Tapicería Cuero Negro'),
        ('tapiceria_alcantara', 'Tapicería Alcantara Roja'),
        ('tapiceria_tela', 'Tapicería Tela Gris'),
        # Extras
        ('extra_techo', 'Techo Panorámico'),
        ('extra_sonido', 'Sistema de Sonido Premium'),
        ('extra_asistente', 'Asistente de Conducción'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPOS, default='ruedas_19')
    descripcion = models.TextField()
    stock_minimo = models.IntegerField(default=0)
    stock_actual = models.IntegerField(default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.get_tipo_display()}"

    @property
    def precio_venta(self):
        """Calcula el precio de venta como el precio de compra más un 30%"""
        return self.precio_compra * Decimal('1.3')

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
    
    # Componentes específicos
    ruedas = models.ForeignKey(Componente, on_delete=models.SET_NULL, null=True, related_name='ordenes_ruedas', limit_choices_to={'tipo__startswith': 'ruedas_'})
    motor = models.ForeignKey(Componente, on_delete=models.SET_NULL, null=True, related_name='ordenes_motor', limit_choices_to={'tipo__startswith': 'motor_'})
    tapiceria = models.ForeignKey(Componente, on_delete=models.SET_NULL, null=True, related_name='ordenes_tapiceria', limit_choices_to={'tipo__startswith': 'tapiceria_'})
    extras = models.ManyToManyField(Componente, related_name='ordenes_extras', limit_choices_to={'tipo__startswith': 'extra_'})
    
    def __str__(self):
        return f"Orden {self.numero_orden} - {self.coche.nombre}"

    def save(self, *args, **kwargs):
        if not self.numero_orden:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero_orden = f"OF-{timestamp}"
        super().save(*args, **kwargs)
    
    def verificar_componentes(self):
        """Verifica si todos los componentes están disponibles"""
        return bool(self.ruedas and self.motor and self.tapiceria and self.extras.exists())

class ComponenteOrden(models.Model):
    orden = models.ForeignKey(OrdenFabricacion, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    es_extra = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.componente.nombre} - {self.orden.numero_orden}"