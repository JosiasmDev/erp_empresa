# ecommerce/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Coche, Pedido
from .forms import PasarelaPagoForm
from sales.models import Pedido as SalesPedido
from crm.models import Cliente

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
    
    # Obtener valores de la sesión
    rueda = request.session.get('rueda', coche.rueda)
    motorizacion = request.session.get('motorizacion', coche.motorizacion)
    tapiceria = request.session.get('tapiceria', coche.tapiceria)
    extras = request.session.get('extras', coche.extras)
    
    # Calcular precio total
    precio_total = coche.precio_base
    if rueda != coche.rueda:
        precio_total += Decimal('1000.00')
    if motorizacion != coche.motorizacion:
        precio_total += Decimal('5000.00')
    if tapiceria != coche.tapiceria:
        precio_total += Decimal('2000.00')
    if extras != coche.extras:
        precio_total += Decimal('3000.00')

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
                # Crear o obtener el cliente
                cliente, created = Cliente.objects.get_or_create(
                    usuario=request.user,
                    defaults={
                        'nombre': nombre_completo,
                        'email': email,
                        'telefono': '',  # Se puede actualizar después
                        'direccion': '',  # Se puede actualizar después
                    }
                )

                # Crear el pedido en ecommerce
                pedido_ecommerce = Pedido.objects.create(
                    cliente=request.user,
                    coche=coche,
                    precio_total=precio_total,
                    rueda_seleccionada=rueda,
                    motorizacion_seleccionada=motorizacion,
                    tapiceria_seleccionada=tapiceria,
                    extras_seleccionados=extras
                )

                # Crear el pedido en sales
                pedido_sales = SalesPedido.objects.create(
                    cliente=cliente,
                    coche=coche,
                    color=coche.color,
                    rueda=rueda,
                    total=precio_total
                )

                # Crear orden de fabricación
                from manufacturing.models import OrdenFabricacion
                orden_fabricacion = OrdenFabricacion.objects.create(
                    pedido=pedido_sales,
                    coche=coche,
                    estado='pendiente'
                )

                # Crear orden de entrega
                from inventory.models import OrdenEntrega
                orden_entrega = OrdenEntrega.objects.create(
                    pedido=pedido_sales,
                    estado='pendiente'
                )

                # Registrar la venta en contabilidad
                from accounting.models import Cuenta
                Cuenta.objects.create(
                    tipo='venta',
                    descripcion=f'Venta del coche {coche.nombre} - Pedido {pedido_ecommerce.numero_pedido}',
                    monto=precio_total,
                    pedido=pedido_ecommerce
                )

                # Limpiar la sesión
                for key in ['rueda', 'motorizacion', 'tapiceria', 'extras', 
                          'rueda_precio', 'motorizacion_precio', 'tapiceria_precio', 
                          'extras_precio', 'precio_total']:
                    if key in request.session:
                        del request.session[key]

                messages.success(request, '¡Compra realizada con éxito!')
                return render(request, 'ecommerce/pago_exitoso.html', {
                    'coche': coche,
                    'nombre_completo': nombre_completo,
                    'precio_total': precio_total,
                    'numero_pedido': pedido_ecommerce.numero_pedido,
                    'orden_fabricacion': orden_fabricacion,
                    'orden_entrega': orden_entrega
                })
            else:
                form.add_error('aceptar_contrato', 'Debes aceptar el contrato para continuar.')
    else:
        form = PasarelaPagoForm(initial={
            'nombre_completo': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        })

    return render(request, 'ecommerce/pasarela_pago.html', {
        'coche': coche,
        'form': form,
        'rueda': rueda,
        'motorizacion': motorizacion,
        'tapiceria': tapiceria,
        'extras': extras,
        'precio_total': precio_total
    })