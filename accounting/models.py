from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal

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
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pedido = models.ForeignKey('ecommerce.Pedido', on_delete=models.SET_NULL, null=True, blank=True)
    empleado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    orden_compra = models.ForeignKey('purchase.OrdenCompra', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.monto}€ - {self.fecha.strftime('%Y-%m-%d')}"

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
        from datetime import datetime
        inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return cls.objects.filter(
            tipo__in=['ingreso', 'venta'],
            fecha__gte=inicio_mes
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

    @classmethod
    def get_gastos_mes(cls):
        """Calcula los gastos del mes actual"""
        from django.utils import timezone
        from datetime import datetime
        inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return cls.objects.filter(
            tipo__in=['gasto', 'salario', 'compra', 'stock'],
            fecha__gte=inicio_mes
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

class Balance(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    ingresos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gastos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salarios_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    compras_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ventas_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Balance {self.fecha.strftime('%Y-%m-%d')} - {self.balance_total}€"
    
    def calcular_totales(self):
        self.ingresos_totales = Cuenta.objects.filter(tipo='ingreso').aggregate(total=models.Sum('monto'))['total'] or 0
        self.gastos_totales = Cuenta.objects.filter(tipo='gasto').aggregate(total=models.Sum('monto'))['total'] or 0
        self.salarios_totales = Cuenta.objects.filter(tipo='salario').aggregate(total=models.Sum('monto'))['total'] or 0
        self.compras_totales = Cuenta.objects.filter(tipo='compra').aggregate(total=models.Sum('monto'))['total'] or 0
        self.ventas_totales = Cuenta.objects.filter(tipo='venta').aggregate(total=models.Sum('monto'))['total'] or 0
        self.balance_total = self.ingresos_totales + self.ventas_totales - self.gastos_totales - self.salarios_totales - self.compras_totales

class Factura(models.Model):
    TIPOS = [
        ('compra', 'Factura de Compra'),
        ('venta', 'Factura de Venta'),
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    descripcion = models.TextField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    orden_compra = models.OneToOneField('purchase.OrdenCompra', on_delete=models.CASCADE, null=True, blank=True)
    cuenta = models.OneToOneField('Cuenta', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Factura {self.numero} - {self.get_tipo_display()}"
    
    def save(self, *args, **kwargs):
        if not self.numero:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero = f"FAC-{timestamp}"
        if not self.iva:
            self.iva = self.subtotal * Decimal('0.21')  # 21% IVA
        if not self.total:
            self.total = self.subtotal + self.iva
        super().save(*args, **kwargs)