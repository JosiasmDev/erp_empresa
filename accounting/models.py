from django.db import models
from django.contrib.auth.models import User

class Cuenta(models.Model):
    TIPOS = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
        ('salario', 'Salario'),
        ('compra', 'Compra'),
        ('venta', 'Venta'),
    ]
    
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pedido = models.ForeignKey('ecommerce.Pedido', on_delete=models.SET_NULL, null=True, blank=True)
    empleado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    orden_compra = models.ForeignKey('purchase.OrdenCompra', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.monto}€ - {self.fecha.strftime('%Y-%m-%d')}"

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