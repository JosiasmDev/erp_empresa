from .models import RelojSimulacion
from django.utils import timezone

def reloj_context(request):
    reloj, created = RelojSimulacion.objects.get_or_create(
        defaults={'fecha_actual': timezone.now(), 'activo': True}
    )
    return {'reloj': reloj} 