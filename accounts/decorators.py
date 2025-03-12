from django.http import HttpResponseForbidden
from .models import Profile

def role_required(allowed_roles):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Debes iniciar sesión.")
            try:
                profile = Profile.objects.get(user=request.user)
                user_permissions = profile.get_permissions()
                if not any(allowed_module in user_permissions for allowed_module in allowed_roles) and \
                   'administrador' not in profile.role and 'gerente' not in profile.role:
                    return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            except Profile.DoesNotExist:
                return HttpResponseForbidden("Perfil no encontrado.")
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator