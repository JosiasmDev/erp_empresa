from django.db import models

class Coche(models.Model):
    TAMANIO_CHOICES = [
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    ]
    COLOR_CHOICES = [
        ('Rojo', 'Rojo'),
        ('Negro', 'Negro'),
        ('Azul', 'Azul'),
        ('Plateado', 'Plateado'),
        ('Blanco', 'Blanco'),
    ]
    RUEDA_CHOICES = [
        ('17"', '17 pulgadas'),
        ('19"', '19 pulgadas'),
        ('21"', '21 pulgadas'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    tamanio = models.CharField(max_length=10, choices=TAMANIO_CHOICES)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    potencia = models.IntegerField(help_text="Potencia en caballos de fuerza (HP)")
    velocidad_maxima = models.IntegerField(help_text="Velocidad máxima en km/h")
    descripcion = models.TextField()
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='Negro')
    rueda = models.CharField(max_length=10, choices=RUEDA_CHOICES, default='19"')
    imagen_3d = models.ImageField(upload_to='coches/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.tamanio})"