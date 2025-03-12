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

    def __str__(self):
        return self.nombre