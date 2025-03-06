from django.db import models

class Campana(models.Model):
    nombre = models.CharField(max_length=100)
    objetivo = models.CharField(max_length=200)
    fecha_envio = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[('Borrador', 'Borrador'), ('Enviada', 'Enviada')], default='Borrador')

    def __str__(self):
        return self.nombre