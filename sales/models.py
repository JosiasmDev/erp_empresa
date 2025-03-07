from django.db import models
from ecommerce.models import Coche
from crm.models import Cliente

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE, null=True, blank=True)  # Temporalmente nullable
    color = models.CharField(max_length=10, choices=Coche.COLOR_CHOICES, default='Negro')
    rueda = models.CharField(max_length=10, choices=Coche.RUEDA_CHOICES, default='19"')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Procesado', 'Procesado'), ('Enviado', 'Enviado')], default='Pendiente')

    def calcular_total(self):
        self.total = self.coche.precio_base  # Simplificado
        self.save()

    def __str__(self):
        return f"Pedido {self.id} - {self.coche.nombre}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE, null=True, blank=True)  # Temporalmente nullable
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"Ítem {self.id} - {self.coche.nombre}"