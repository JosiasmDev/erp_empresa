from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal

class RelojSimulacion(models.Model):
    fecha_actual = models.DateTimeField(default=timezone.now)
    velocidad_simulacion = models.IntegerField(default=3)  # 3 segundos = 1 hora
    activo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Reloj de Simulación"
        verbose_name_plural = "Reloj de Simulación"

    def __str__(self):
        return f"Reloj Simulación - {self.fecha_actual}"

    def avanzar_tiempo(self):
        """Avanza el tiempo simulado"""
        if self.activo:
            self.fecha_actual = self.fecha_actual + timezone.timedelta(hours=1)
            self.save()

class Employee(models.Model):
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=50)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    salario_acumulado = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    fecha_contratacion = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.puesto}"

class Inventory(models.Model):
    material = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.material} - Stock: {self.cantidad}"

    class Meta:
        verbose_name_plural = "Inventories"

class PurchaseOrder(models.Model):
    material = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pedido = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada')
    ])

    def __str__(self):
        return f"Orden #{self.id} - {self.material}"

class ProductionOrder(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    fecha_inicio = models.DateTimeField()
    fecha_completado = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada')
    ])
    materiales_disponibles = models.BooleanField(default=False)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"Producción #{self.id} - {self.producto}" 