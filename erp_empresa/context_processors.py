# erp_empresa/context_processors.py
def user_roles(request):
    if request.user.is_authenticated:
        is_gerencia_or_admin = request.user.groups.filter(name__in=['Administrador', 'Gerencia']).exists()
    else:
        is_gerencia_or_admin = False
    return {
        'is_gerencia_or_admin': is_gerencia_or_admin,
    }