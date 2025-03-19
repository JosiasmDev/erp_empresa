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
    stock_minimo = models.IntegerField(default=10)
    stock_maximo = models.IntegerField(default=100)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    ubicacion = models.CharField(max_length=50, blank=True)
    notas = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.componente.get_tipo_display()} - Stock: {self.cantidad}"
    
    def actualizar_stock(self, cantidad, tipo_movimiento):
        if tipo_movimiento == 'entrada':
            self.cantidad += cantidad
        elif tipo_movimiento == 'salida':
            if self.cantidad >= cantidad:
                self.cantidad -= cantidad
            else:
                raise ValueError("Stock insuficiente")
        self.save()

class MovimientoStock(models.Model):
    TIPOS = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
        ('transferencia', 'Transferencia'),
    ]
    
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha = models.DateTimeField(auto_now_add=True)
    orden_entrega = models.ForeignKey(OrdenEntrega, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    numero_referencia = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.componente.nombre} - {self.cantidad}"
    
    def save(self, *args, **kwargs):
        if not self.precio_total and self.cantidad and self.costo_unitario:
            self.precio_total = self.cantidad * self.costo_unitario
        # Actualizar el stock del componente
        stock, created = Stock.objects.get_or_create(componente=self.componente)
        stock.actualizar_stock(self.cantidad, self.tipo)
        super().save(*args, **kwargs)