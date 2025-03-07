import os
import django
from faker import Faker
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

from ecommerce.models import Coche
from website.models import Pagina
from crm.models import Cliente
from sales.models import Pedido, PedidoItem
from human_resources.models import Empleado
from manufacturing.models import OrdenProduccion
from marketing_automation.models import Campana
from inventory.models import Pieza, MovimientoStock
from accounting.models import Factura
from purchase.models import Compra

fake = Faker()

# Crear solo dos coches (Eclipse y Arrow)
coches = [
    {
        'nombre': 'Eclipse',
        'precio_base': 78000,
        'potencia': 470,
        'velocidad_maxima': 300,
        'descripcion': 'Un sedán deportivo con interiores lujosos y potencia brutal.'
    },
    {
        'nombre': 'Arrow',
        'precio_base': 48000,
        'potencia': 320,
        'velocidad_maxima': 260,
        'descripcion': 'Pequeño pero feroz, con aerodinámica optimizada y tracción total.'
    },
]

# Eliminar coches existentes para evitar duplicados
Coche.objects.all().delete()

for coche_data in coches:
    Coche.objects.create(
        nombre=coche_data['nombre'],
        precio_base=coche_data['precio_base'],
        potencia=coche_data['potencia'],
        velocidad_maxima=coche_data['velocidad_maxima'],
        descripcion=coche_data['descripcion'],
        color='Negro',
        rueda='19"'
    )

# Crear páginas para cada coche en el website
for coche in Coche.objects.all():
    Pagina.objects.create(
        coche=coche,
        titulo=f"{coche.nombre} - SAG",
        contenido=f"Descubre el {coche.nombre}, un coche deportivo con {coche.potencia} HP y una velocidad máxima de {coche.velocidad_maxima} km/h. {coche.descripcion}",
        publicada=True
    )

# Crear clientes, empleados, campañas, pedidos, etc. (simplificado)
for _ in range(5):
    Cliente.objects.create(
        nombre=fake.name(),
        email=fake.email(),
        telefono=fake.phone_number()[:15]
    )

for _ in range(3):
    Empleado.objects.create(
        nombre=fake.name(),
        cargo=fake.job(),
        salario=random.uniform(3000, 8000)
    )

for _ in range(2):
    Campana.objects.create(
        nombre=fake.catch_phrase(),
        objetivo=f"Promocionar {random.choice(coches)['nombre']}",
        fecha_envio=fake.date_time_this_month(),
        estado=random.choice(['Borrador', 'Enviada'])
    )

clientes = Cliente.objects.all()
for _ in range(3):
    cliente = random.choice(clientes)
    coche = random.choice(Coche.objects.all())
    pedido = Pedido.objects.create(
        cliente=cliente,
        coche=coche,
        color=random.choice(['Rojo', 'Negro', 'Azul']),
        rueda=random.choice(['17"', '19"', '21"'])
    )
    PedidoItem.objects.create(pedido=pedido, coche=coche, cantidad=1)
    pedido.calcular_total()
    Factura.objects.create(pedido=pedido, monto=pedido.total, pagada=random.choice([True, False]))

for coche in Coche.objects.all():
    OrdenProduccion.objects.create(coche=coche, cantidad=random.randint(5, 20))

print("Datos de SAG actualizados con Eclipse y Arrow.")