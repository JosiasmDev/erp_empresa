from django.db import models
from crm.models import Cliente
from ecommerce.models import Producto

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Procesado', 'Procesado'), ('Enviado', 'Enviado')], default='Pendiente')

    def calcular_total(self):
        self.total = sum(item.subtotal() for item in self.pedidoitem_set.all())
        self.save()

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio
        super().save(*args, **kwargs)
        self.pedido.calcular_total()