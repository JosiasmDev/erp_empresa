# ecommerce/models.py
from django.db import models

class Coche(models.Model):
    nombre = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    potencia = models.IntegerField()  # HP
    velocidad_maxima = models.IntegerField()  # km/h
    descripcion = models.TextField()
    color = models.CharField(max_length=50, default='Negro', choices=[
        ('Negro', 'Negro'),
        ('Rojo', 'Rojo'),
        ('Azul', 'Azul'),
        ('Blanco', 'Blanco'),
    ])
    rueda = models.CharField(max_length=10, default='19"', choices=[
        ('17"', '17"'),
        ('19"', '19"'),
        ('21"', '21"'),
    ])
    motorizacion = models.CharField(max_length=50, default='V6 3.0L', choices=[
        ('V6 3.0L', 'V6 3.0L'),
        ('V8 4.0L', 'V8 4.0L'),
        ('Eléctrico 400kW', 'Eléctrico 400kW'),
    ])
    tapiceria = models.CharField(max_length=50, default='Cuero Negro', choices=[
        ('Cuero Negro', 'Cuero Negro'),
        ('Alcantara Roja', 'Alcantara Roja'),
        ('Tela Gris', 'Tela Gris'),
    ])
    extras = models.CharField(max_length=200, default='Ninguno', choices=[
        ('Ninguno', 'Ninguno'),
        ('Techo Panorámico', 'Techo Panorámico'),
        ('Sistema de Sonido Premium', 'Sistema de Sonido Premium'),
        ('Asistente de Conducción', 'Asistente de Conducción'),
    ])

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_produccion', 'En Producción'),
        ('en_almacen', 'En Almacén'),
        ('en_entrega', 'En Entrega'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    numero_pedido = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE, related_name='pedidos_ecommerce')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    rueda_seleccionada = models.CharField(max_length=10)
    motorizacion_seleccionada = models.CharField(max_length=50)
    tapiceria_seleccionada = models.CharField(max_length=50)
    extras_seleccionados = models.CharField(max_length=200)
    orden_entrega = models.OneToOneField('inventory.OrdenEntrega', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedido_entrega')

    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.cliente.username}"

    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            # Generar número de pedido único
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero_pedido = f"PED-{timestamp}"
        super().save(*args, **kwargs)