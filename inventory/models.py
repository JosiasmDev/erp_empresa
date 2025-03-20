from django.db import models
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
    tipo = models.CharField(max_length=50, choices=TIPOS)
    descripcion = models.TextField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.get_tipo_display()}"

class Stock(models.Model):
    componente = models.OneToOneField('inventory.Componente', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    stock_maximo = models.IntegerField(default=20)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.componente.nombre} - {self.cantidad} unidades"
    
    @property
    def necesita_reposicion(self):
        return self.cantidad <= self.stock_minimo

class MovimientoStock(models.Model):
    TIPOS = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida')
    ]
    
    componente = models.ForeignKey('inventory.Componente', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.get_tipo_display()} de {self.componente.nombre} - {self.cantidad} unidades"
    
    def save(self, *args, **kwargs):
        # Calcular precio total
        self.precio_total = self.cantidad * self.precio_unitario
        
        # Actualizar stock
        stock, created = Stock.objects.get_or_create(componente=self.componente)
        if self.tipo == 'entrada':
            stock.cantidad += self.cantidad
        else:
            stock.cantidad -= self.cantidad
        stock.save()
        
        super().save(*args, **kwargs)

class OrdenEntrega(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ]
    
    pedido = models.OneToOneField('sales.Pedido', on_delete=models.CASCADE, related_name='orden_entrega_pedido')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Orden de Entrega - Pedido {self.pedido.numero_pedido}"