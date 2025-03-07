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

# Crear coches deportivos SAG
coches = [
    {'nombre': 'SAG Striker S', 'tamanio': 'Pequeño', 'precio_base': 45000, 'potencia': 300, 'velocidad_maxima': 250, 'descripcion': 'Un coupé deportivo compacto con diseño agresivo y motor eléctrico de alta respuesta.'},
    {'nombre': 'SAG Arrow XS', 'tamanio': 'Pequeño', 'precio_base': 48000, 'potencia': 320, 'velocidad_maxima': 260, 'descripcion': 'Pequeño pero feroz, con aerodinámica optimizada y tracción total.'},
    {'nombre': 'SAG Phantom M', 'tamanio': 'Mediano', 'precio_base': 75000, 'potencia': 450, 'velocidad_maxima': 290, 'descripcion': 'Un sedán deportivo de mediano tamaño con interiores lujosos y potencia brutal.'},
    {'nombre': 'SAG Eclipse M', 'tamanio': 'Mediano', 'precio_base': 78000, 'potencia': 470, 'velocidad_maxima': 300, 'descripcion': 'Elegancia y fuerza combinadas en un diseño futurista de mediano tamaño.'},
    {'nombre': 'SAG Titan G', 'tamanio': 'Grande', 'precio_base': 120000, 'potencia': 600, 'velocidad_maxima': 320, 'descripcion': 'Un SUV deportivo de gran tamaño con tecnología avanzada y rendimiento extremo.'},
    {'nombre': 'SAG Vortex G', 'tamanio': 'Grande', 'precio_base': 125000, 'potencia': 620, 'velocidad_maxima': 330, 'descripcion': 'El rey de los SUVs deportivos, diseñado para conquistar cualquier terreno.'},
]

for coche_data in coches:
    Coche.objects.create(
        nombre=coche_data['nombre'],
        tamanio=coche_data['tamanio'],
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
        contenido=f"Descubre el {coche.nombre}, un coche deportivo {coche.tamanio.lower()} con {coche.potencia} HP y una velocidad máxima de {coche.velocidad_maxima} km/h. {coche.descripcion}",
        publicada=True
    )

# Crear clientes
for _ in range(10):
    Cliente.objects.create(
        nombre=fake.name(),
        email=fake.email(),
        telefono=fake.phone_number()[:15]
    )

# Crear empleados
for _ in range(5):
    Empleado.objects.create(
        nombre=fake.name(),
        cargo=fake.job(),
        salario=random.uniform(3000, 8000)
    )

# Crear campañas de marketing
for _ in range(3):
    Campana.objects.create(
        nombre=fake.catch_phrase(),
        objetivo=f"Promocionar {random.choice(coches)['nombre']}",
        fecha_envio=fake.date_time_this_month(),
        estado=random.choice(['Borrador', 'Enviada'])
    )

# Crear pedidos y facturas
clientes = Cliente.objects.all()
for _ in range(5):
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

# Crear órdenes de producción
for coche in Coche.objects.all():
    OrdenProduccion.objects.create(coche=coche, cantidad=random.randint(5, 20))

# Crear piezas y movimientos
piezas = ['Motor V6', 'Transmisión', 'Ruedas 19"', 'Batería Eléctrica']
for pieza_nombre in piezas:
    Pieza.objects.create(nombre=pieza_nombre, cantidad_disponible=random.randint(50, 200))
for _ in range(20):
    pieza = random.choice(Pieza.objects.all())
    MovimientoStock.objects.create(pieza=pieza, cantidad=random.randint(10, 50), tipo=random.choice(['Entrada', 'Salida']))

# Crear compras
for _ in range(5):
    pieza = random.choice(Pieza.objects.all())
    Compra.objects.create(
        pieza=pieza,
        cantidad=random.randint(10, 50),
        proveedor=fake.company(),
        costo=random.uniform(100, 1000)
    )

print("Datos de SAG creados exitosamente.")