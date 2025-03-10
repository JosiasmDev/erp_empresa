from django.db import models
from ecommerce.models import Coche
from crm.models import Cliente

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