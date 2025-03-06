from django.db import models

class Campana(models.Model):
    nombre = models.CharField(max_length=100)
    objetivo = models.CharField(max_length=200)
    fecha_envio = models.DateTimeField()