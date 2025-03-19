from django.db import models

class RelojSimulacion(models.Model):
    fecha_actual = models.DateTimeField()
    velocidad_simulacion = models.IntegerField(default=3)  # 1 hora real = 3 segundos
    activo = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reloj: {self.fecha_actual.strftime('%Y-%m-%d %H:%M')} - {'Activo' if self.activo else 'Inactivo'}"

    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(id=1)
        return instance

    def avanzar_tiempo(self):
        from datetime import timedelta
        self.fecha_actual += timedelta(hours=1)
        self.save() 