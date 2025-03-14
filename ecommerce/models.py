# ecommerce/models.py
from django.db import models

class Coche(models.Model):
    nombre = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    potencia = models.IntegerField()  # HP
    velocidad_maxima = models.IntegerField()  # km/h
    descripcion = models.TextField()
    color = models.CharField(max_length=50, default='Negro', choices=[
        ('Negro', 'Negro'),
        ('Rojo', 'Rojo'),
        ('Azul', 'Azul'),
        ('Blanco', 'Blanco'),
    ])
    rueda = models.CharField(max_length=10, default='19"', choices=[
        ('17"', '17"'),
        ('19"', '19"'),
        ('21"', '21"'),
    ])
    motorizacion = models.CharField(max_length=50, default='V6 3.0L', choices=[
        ('V6 3.0L', 'V6 3.0L'),
        ('V8 4.0L', 'V8 4.0L'),
        ('Eléctrico 400kW', 'Eléctrico 400kW'),
    ])
    tapiceria = models.CharField(max_length=50, default='Cuero Negro', choices=[
        ('Cuero Negro', 'Cuero Negro'),
        ('Alcantara Roja', 'Alcantara Roja'),
        ('Tela Gris', 'Tela Gris'),
    ])
    extras = models.CharField(max_length=200, default='Ninguno', choices=[
        ('Ninguno', 'Ninguno'),
        ('Techo Panorámico', 'Techo Panorámico'),
        ('Sistema de Sonido Premium', 'Sistema de Sonido Premium'),
        ('Asistente de Conducción', 'Asistente de Conducción'),
    ])

    def __str__(self):
        return self.nombre