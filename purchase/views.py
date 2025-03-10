from django.shortcuts import render, redirect, get_object_or_404
from .models import Compra
from .forms import CompraForm
from ecommerce.models import Coche
from crm.models import Cliente
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounting.models import Factura
from manufacturing.models import OrdenProduccion
from inventory.models import MovimientoStock
import threading
import time

def simulate_production(compra):
    orden = OrdenProduccion.objects.create(coche=compra.coche, cantidad=1)
    proveedor_cost = compra.precio_total * 0.3
    MovimientoStock.objects.create(producto=f"Material {compra.coche.nombre}", cantidad=1, tipo='entrada')
    
    def update_status():
        time.sleep(10)  # Entrega de materiales
        MovimientoStock.objects.filter(producto=f"Material {compra.coche.nombre}").update(cantidad=0)
        Factura.objects.create(pedido=None, monto=-proveedor_cost, pagada=True)
        orden.completada = True
        orden.save()
        time.sleep(20)  # Terminación de orden
        messages.success(None, f'Vehículo {compra.coche.nombre} entregado a {compra.cliente.nombre}.')

    threading.Thread(target=update_status).start()

@login_required
def process_payment(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    if request.method == 'POST':
        compra.pagado = True
        compra.save()
        Factura.objects.create(pedido=None, monto=compra.precio_total, pagada=True)
        simulate_production(compra)
        messages.success(request, 'Pago procesado. La entrega está en curso.')
        return redirect('website_index')
    return render(request, 'purchase/process_payment.html', {'compra': compra})

def purchase_form(request, coche_id):
    coche = Coche.objects.get(id=coche_id)
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.coche = coche
            compra.precio_total = float(request.POST.get('precio_total', coche.precio_base))
            compra.save()
            messages.success(request, 'Compra iniciada. Por favor, inicia sesión para pagar.' if not request.user.is_authenticated else 'Compra iniciada.')
            return redirect('login' if not request.user.is_authenticated else 'purchase_process_payment', compra.id)
    else:
        form = CompraForm(initial={'coche': coche, 'precio_total': coche.precio_base})
    return render(request, 'purchase/purchase_form.html', {'form': form, 'coche': coche})

def compras(request):
    compras = Compra.objects.all()
    if request.user.is_authenticated:
        context = {
            'compras': compras,
            'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
            'is_cliente': request.user.groups.filter(name='Clientes').exists(),
            'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
            'is_compras': request.user.groups.filter(name='Compras').exists(),
            'is_logistica': request.user.groups.filter(name='Logistica').exists(),
        }
    else:
        context = {'compras': compras}
    return render(request, 'purchase/compras.html', context)