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
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE, related_name='componentes')
    nombre = models.CharField(max_length=100)  # Ejemplo: "Ruedas", "Techo Solar", "Motor"
    opcion = models.CharField(max_length=100)  # Ejemplo: "Estándar 17"", "Panorámico", "V6 3.0L"
    precio_adicional = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombre}: {self.opcion} (+{self.precio_adicional}€)"