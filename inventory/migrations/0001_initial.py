# Generated by Django 5.1.7 on 2025-03-26 22:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Componente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('ruedas_17', 'Ruedas 17"'), ('ruedas_19', 'Ruedas 19"'), ('ruedas_21', 'Ruedas 21"'), ('motor_v6', 'Motor V6 3.0L'), ('motor_v8', 'Motor V8 4.0L'), ('motor_electrico', 'Motor Eléctrico 400kW'), ('tapiceria_cuero_negro', 'Tapicería Cuero Negro'), ('tapiceria_alcantara', 'Tapicería Alcantara Roja'), ('tapiceria_tela', 'Tapicería Tela Gris'), ('extra_techo', 'Techo Panorámico'), ('extra_sonido', 'Sistema de Sonido Premium'), ('extra_asistente', 'Asistente de Conducción')], max_length=50)),
                ('descripcion', models.TextField()),
                ('precio_venta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_compra', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], max_length=10)),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.componente')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_entrega', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_proceso', 'En Proceso'), ('completada', 'Completada'), ('cancelada', 'Cancelada')], default='pendiente', max_length=20)),
                ('notas', models.TextField(blank=True, null=True)),
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='orden_entrega_pedido', to='sales.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('stock_minimo', models.IntegerField(default=5)),
                ('stock_maximo', models.IntegerField(default=200)),
                ('ubicacion', models.CharField(blank=True, max_length=100, null=True)),
                ('notas', models.TextField(blank=True, null=True)),
                ('componente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.componente')),
            ],
        ),
    ]
