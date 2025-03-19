# ecommerce/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Coche, Pedido
from .forms import PasarelaPagoForm

@login_required
def ecommerce_dashboard(request):
    coches = Coche.objects.all()
    context = {
        'coches': coches,
    }
    return render(request, 'ecommerce/dashboard.html', context)

@login_required
def pasarela_pago(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)

    # Obtener los precios de la sesión al inicio
    rueda_precio = request.session.get('rueda_precio', 0)
    motorizacion_precio = request.session.get('motorizacion_precio', 0)
    tapiceria_precio = request.session.get('tapiceria_precio', 0)
    extras_precio = request.session.get('extras_precio', 0)
    precio_total = request.session.get('precio_total', coche.precio_base)

    # Obtener las selecciones de POST o sesión
    rueda = request.POST.get('rueda', request.session.get('rueda', coche.rueda))
    motorizacion = request.POST.get('motorizacion', request.session.get('motorizacion', coche.motorizacion))
    tapiceria = request.POST.get('tapiceria', request.session.get('tapiceria', coche.tapiceria))
    extras = request.POST.get('extras', request.session.get('extras', coche.extras))

    if request.method == 'POST':
        form = PasarelaPagoForm(request.POST)
        if form.is_valid():
            nombre_completo = form.cleaned_data['nombre_completo']
            email = form.cleaned_data['email']
            numero_tarjeta = form.cleaned_data['numero_tarjeta']
            fecha_expiracion = form.cleaned_data['fecha_expiracion']
            cvv = form.cleaned_data['cvv']
            aceptar_contrato = form.cleaned_data['aceptar_contrato']

            if aceptar_contrato:
                # Crear el pedido
                pedido = Pedido.objects.create(
                    cliente=request.user,
                    coche=coche,
                    precio_total=precio_total,
                    rueda_seleccionada=rueda,
                    motorizacion_seleccionada=motorizacion,
                    tapiceria_seleccionada=tapiceria,
                    extras_seleccionados=extras
                )

                # Limpiar la sesión
                for key in ['rueda', 'motorizacion', 'tapiceria', 'extras', 
                          'rueda_precio', 'motorizacion_precio', 'tapiceria_precio', 
                          'extras_precio', 'precio_total']:
                    if key in request.session:
                        del request.session[key]

                return render(request, 'ecommerce/pago_exitoso.html', {
                    'coche': coche,
                    'nombre_completo': nombre_completo,
                    'precio_total': precio_total,
                    'numero_pedido': pedido.numero_pedido
                })
            else:
                form.add_error('aceptar_contrato', 'Debes aceptar el contrato para continuar.')
    else:
        form = PasarelaPagoForm(initial={
            'nombre_completo': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        })

    context = {
        'coche': coche,
        'form': form,
        'precio_total': precio_total,
        'rueda_precio': rueda_precio,
        'motorizacion_precio': motorizacion_precio,
        'tapiceria_precio': tapiceria_precio,
        'extras_precio': extras_precio,
        'rueda': rueda,
        'motorizacion': motorizacion,
        'tapiceria': tapiceria,
        'extras': extras,
    }
    return render(request, 'ecommerce/pasarela_pago.html', context)