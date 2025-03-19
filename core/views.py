from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import F
from django.utils import timezone
from decimal import Decimal
from .models import Employee, ProductionOrder, PurchaseOrder, Inventory

@csrf_exempt
@require_POST
def actualizar_tareas(request):
    try:
        # 1. Pagar salarios a empleados (por minuto)
        empleados = Employee.objects.filter(activo=True)
        for empleado in empleados:
            # Calcular el salario por minuto (salario mensual / (30 días * 24 horas * 60 minutos))
            salario_por_minuto = empleado.salario_base / Decimal('43200')
            empleado.salario_acumulado = F('salario_acumulado') + salario_por_minuto
            empleado.save()

        # 2. Procesar órdenes de producción pendientes
        ordenes_produccion = ProductionOrder.objects.filter(
            estado='en_proceso',
            materiales_disponibles=True,
            completada=False
        )
        for orden in ordenes_produccion:
            orden.completada = True
            orden.fecha_completado = timezone.now()
            orden.estado = 'completada'
            orden.save()

        # 3. Entregar materiales de proveedores a almacén
        ordenes_compra = PurchaseOrder.objects.filter(estado='pendiente')
        for orden in ordenes_compra:
            # Actualizar inventario
            Inventory.objects.filter(material=orden.material).update(
                cantidad=F('cantidad') + orden.cantidad
            )
            orden.estado = 'completada'
            orden.save()

        # 4. Transferir materiales de almacén a producción
        ordenes_produccion = ProductionOrder.objects.filter(
            estado='pendiente',
            materiales_disponibles=False
        )
        for orden in ordenes_produccion:
            # Verificar disponibilidad de materiales (simulado)
            materiales_necesarios = {
                'Motor': 1,
                'Transmisión': 1,
                'Chasis': 1,
                'Ruedas': 4,
                'Asientos': 5,
                'Volante': 1,
                'Sistema Eléctrico': 1
            }
            
            materiales_suficientes = True
            materiales_a_descontar = {}
            
            # Verificar disponibilidad
            for material, cantidad in materiales_necesarios.items():
                cantidad_necesaria = cantidad * orden.cantidad
                try:
                    inventario = Inventory.objects.get(material=material)
                    if inventario.cantidad < cantidad_necesaria:
                        materiales_suficientes = False
                        break
                    materiales_a_descontar[material] = cantidad_necesaria
                except Inventory.DoesNotExist:
                    materiales_suficientes = False
                    break

            if materiales_suficientes:
                # Descontar materiales
                for material, cantidad in materiales_a_descontar.items():
                    Inventory.objects.filter(material=material).update(
                        cantidad=F('cantidad') - cantidad
                    )
                orden.materiales_disponibles = True
                orden.estado = 'en_proceso'
                orden.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Tareas actualizadas correctamente',
            'detalles': {
                'empleados_actualizados': empleados.count(),
                'ordenes_produccion_completadas': ordenes_produccion.filter(completada=True).count(),
                'ordenes_compra_procesadas': ordenes_compra.count()
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500) 