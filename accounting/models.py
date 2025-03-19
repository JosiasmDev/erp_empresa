from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from ecommerce.models import Pedido
from purchase.models import OrdenCompra

class Cuenta(models.Model):
    TIPOS = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
        ('salario', 'Salario'),
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('stock', 'Stock'),
    ]
    
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    concepto = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    empleado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.concepto} - {self.monto}€"

    @classmethod
    def get_balance_total(cls):
        """Calcula el balance total de la empresa"""
        ingresos = cls.objects.filter(tipo__in=['ingreso', 'venta']).aggregate(total=Sum('monto'))['total'] or Decimal('0')
        gastos = cls.objects.filter(tipo__in=['gasto', 'salario', 'compra', 'stock']).aggregate(total=Sum('monto'))['total'] or Decimal('0')
        return ingresos - gastos

    @classmethod
    def get_ingresos_mes(cls):
        """Calcula los ingresos del mes actual"""
        from django.utils import timezone
        inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return cls.objects.filter(
            tipo__in=['ingreso', 'venta'],
            fecha__gte=inicio_mes
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

    @classmethod
    def get_gastos_mes(cls):
        """Calcula los gastos del mes actual"""
        from django.utils import timezone
        inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return cls.objects.filter(
            tipo__in=['gasto', 'salario', 'compra', 'stock'],
            fecha__gte=inicio_mes
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

class Balance(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    ingresos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gastos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        get_latest_by = 'fecha'
    
    def __str__(self):
        return f"Balance {self.fecha.strftime('%d/%m/%Y')} - Saldo: {self.saldo}€"

    def actualizar_saldo(self):
        self.saldo = self.ingresos - self.gastos
        self.save()

@receiver(post_save, sender=Pedido)
def registrar_ingreso_pedido(sender, instance, created, **kwargs):
    if instance.estado == 'completado':
        Cuenta.objects.create(
            tipo='venta',
            concepto=f'Venta de coche - Pedido #{instance.numero_pedido}',
            monto=instance.precio_total,
            pedido=instance
        )
        
        try:
            balance = Balance.objects.latest()
        except Balance.DoesNotExist:
            balance = Balance.objects.create()
        
        balance.ingresos += instance.precio_total
        balance.actualizar_saldo()

@receiver(post_save, sender=OrdenCompra)
def registrar_gasto_compra(sender, instance, created, **kwargs):
    if instance.estado == 'aprobada':
        Cuenta.objects.create(
            tipo='compra',
            concepto=f'Compra de componentes - Orden #{instance.numero_orden}',
            monto=instance.total,
            orden_compra=instance
        )
        
        try:
            balance = Balance.objects.latest()
        except Balance.DoesNotExist:
            balance = Balance.objects.create()
        
        balance.gastos += instance.total
        balance.actualizar_saldo()