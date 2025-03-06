from django.db import models

class Pagina(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    publicada = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo