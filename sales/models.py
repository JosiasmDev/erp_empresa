from django.db import models

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey('crm.Cliente', on_delete=models.CASCADE)
    coche = models.ForeignKey('ecommerce.Coche', on_delete=models.CASCADE)
    color = models.CharField(max_length=50, choices=[
        ('Negro', 'Negro'),
        ('Rojo', 'Rojo'),
        ('Azul', 'Azul'),
        ('Blanco', 'Blanco'),
    ], default='Negro')
    rueda = models.CharField(max_length=10, choices=[
        ('17"', '17"'),
        ('19"', '19"'),
        ('21"', '21"'),
    ], default='19"')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def calcular_total(self):
        from ecommerce.models import Coche
        self.total = self.coche.precio_base
        self.save()

    def __str__(self):
        return f"Pedido {self.id} - {self.coche.nombre}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    coche = models.ForeignKey('ecommerce.Coche', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"Item {self.id} - {self.coche.nombre}"