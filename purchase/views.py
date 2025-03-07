from django.shortcuts import render, redirect
from .forms import CompraForm
from ecommerce.models import Coche
from crm.models import Cliente
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounting.models import Factura
from manufacturing.models import OrdenProduccion
from inventory.models import MovimientoStock
from purchase.models import Compra
import time

def purchase_form(request, coche_id):
    coche = Coche.objects.get(id=coche_id)
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.coche = coche
            compra.precio_total = float(request.POST.get('precio_total', coche.precio_base))  # Usar precio_base si no se especifica
            compra.save()
            messages.success(request, 'Compra iniciada. Por favor, inicia sesión para pagar.')
            return redirect('login')
    else:
        form = CompraForm(initial={'coche': coche, 'precio_total': coche.precio_base})
    return render(request, 'purchase/purchase_form.html', {'form': form, 'coche': coche})

@login_required
def process_payment(request, compra_id):
    compra = Compra.objects.get(id=compra_id)
    if request.method == 'POST':
        compra.pagado = True
        compra.save()

        # Ingresar dinero a cuentas
        Factura.objects.create(pedido=None, monto=compra.precio_total, pagada=True)

        # Generar orden de trabajo
        orden = OrdenProduccion.objects.create(coche=compra.coche, cantidad=1)

        # Crear pedidos a proveedores (30% del precio)
        proveedor_cost = compra.precio_total * 0.3
        MovimientoStock.objects.create(producto=f"Material {compra.coche.nombre}", cantidad=1, tipo='entrada')

        # Simulación de entrega de materiales cada 10 segundos
        while not orden.completada:
            time.sleep(10)
            MovimientoStock.objects.filter(producto=f"Material {compra.coche.nombre}").update(cantidad=models.F('cantidad') - 1)
            Factura.objects.create(pedido=None, monto=-proveedor_cost, pagada=True)
            if MovimientoStock.objects.filter(producto=f"Material {compra.coche.nombre}").count() == 0:
                orden.completada = True
                orden.save()
                break

        # Simulación de terminación de orden cada 20 segundos
        time.sleep(20)
        orden.completada = True
        orden.save()
        messages.success(request, f'Vehículo {compra.coche.nombre} entregado a {compra.cliente.nombre}.')
        return redirect('website_index')

    return render(request, 'purchase/process_payment.html', {'compra': compra})