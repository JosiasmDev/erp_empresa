import os
import django
from faker import Faker
import random
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

# Importar modelos
from website.models import Pagina
from crm.models import Cliente
from ecommerce.models import Producto
from sales.models import Pedido, PedidoItem
from human_resources.models import Empleado
from manufacturing.models import OrdenProduccion
from marketing_automation.models import Campana
from inventory.models import MovimientoStock
from accounting.models import Factura
from purchase.models import Compra

fake = Faker()

# Función para poblar datos
def populate_data():
    # 1. Website - 50 páginas
    for _ in range(50):
        Pagina.objects.create(
            titulo=fake.sentence(nb_words=4),
            contenido=fake.paragraph(nb_sentences=5)
        )

    # 2. CRM - 100 clientes
    for _ in range(100):
        Cliente.objects.create(
            nombre=fake.name(),
            email=fake.email(),
            telefono=fake.phone_number()[:15]
        )

    # 3. E-commerce - 200 productos
    for _ in range(200):
        Producto.objects.create(
            nombre=fake.word().capitalize() + " " + fake.word(),
            precio=random.uniform(10, 1000),
            stock=random.randint(0, 500)
        )

    # 4. Human Resources - 50 empleados
    for _ in range(50):
        Empleado.objects.create(
            nombre=fake.name(),
            cargo=fake.job(),
            salario=random.uniform(1000, 10000)
        )

    # 5. Sales - 300 pedidos con ítems
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    for _ in range(300):
        cliente = random.choice(clientes)
        pedido = Pedido.objects.create(
            cliente=cliente,
            total=0,
            fecha=fake.date_time_this_year()
        )
        for _ in range(random.randint(1, 5)):  # 1-5 ítems por pedido
            producto = random.choice(productos)
            cantidad = random.randint(1, 10)
            PedidoItem.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad
            )
        pedido.total = sum(item.producto.precio * item.cantidad for item in pedido.pedidoitem_set.all())
        pedido.save()

    # 6. Manufacturing - 100 órdenes de producción
    for _ in range(100):
        OrdenProduccion.objects.create(
            producto=random.choice(productos),
            cantidad=random.randint(10, 100),
            fecha_inicio=fake.date_time_this_year()
        )

    # 7. Marketing Automation - 30 campañas
    for _ in range(30):
        Campana.objects.create(
            nombre=fake.catch_phrase(),
            objetivo=fake.sentence(),
            fecha_envio=fake.date_time_this_month()
        )

    # 8. Inventory - 500 movimientos de stock
    for _ in range(500):
        MovimientoStock.objects.create(
            producto=random.choice(productos),
            cantidad=random.randint(1, 50),
            tipo=random.choice(['Entrada', 'Salida'])
        )

    # 9. Accounting - 200 facturas
    pedidos = Pedido.objects.all()
    for _ in range(200):
        pedido = random.choice(pedidos)
        Factura.objects.create(
            pedido=pedido,
            monto=pedido.total,
            fecha=fake.date_time_this_year()
        )

    # 10. Purchase - 150 compras
    for _ in range(150):
        Compra.objects.create(
            producto=random.choice(productos),
            cantidad=random.randint(5, 100),
            proveedor=fake.company(),
            fecha=fake.date_time_this_year()
        )

    print("Datos ficticios creados exitosamente.")

if __name__ == '__main__':
    populate_data()