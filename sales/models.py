from django.db import models
from ecommerce.models import Coche

class Pedido(models.Model):
    cliente = models.ForeignKey('crm.Cliente', on_delete=models.CASCADE)
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE)
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

    def calcular_total(self):
        self.total = self.coche.precio_base
        self.save()

    def __str__(self):
        return f"Pedido {self.id} - {self.coche.nombre}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"Item {self.id} - {self.coche.nombre}"