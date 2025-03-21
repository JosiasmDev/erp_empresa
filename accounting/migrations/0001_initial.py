# Generated by Django 4.2 on 2025-03-20 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('ingresos_totales', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('gastos_totales', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('salarios_totales', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('compras_totales', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ventas_totales', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('balance_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto'), ('salario', 'Salario'), ('compra', 'Compra'), ('venta', 'Venta'), ('stock', 'Stock')], max_length=10)),
                ('descripcion', models.TextField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Cuenta',
                'verbose_name_plural': 'Cuentas',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20, unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('compra', 'Factura de Compra'), ('venta', 'Factura de Venta')], max_length=10)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('pagada', 'Pagada'), ('cancelada', 'Cancelada')], default='pendiente', max_length=10)),
                ('descripcion', models.TextField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('iva', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cuenta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounting.cuenta')),
            ],
        ),
    ]
