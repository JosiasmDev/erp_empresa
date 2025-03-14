from django.db import models
from ecommerce.models import Coche

class Pagina(models.Model):
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    publicada = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class Coche(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class PersonalizacionComponente(models.Model):
    coche = models.ForeignKey(Coche, related_name='componentes', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    opcion = models.CharField(max_length=100)
    precio_adicional = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, choices=[('ruedas', 'Ruedas'), ('techo', 'Techo'), ('motor', 'Motor')], default='ruedas')  # Añade este campo

    def __str__(self):
        return f"{self.nombre} - {self.opcion}"