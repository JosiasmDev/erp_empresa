# ERP Empresa - Sistema de Gestión Empresarial

Sistema ERP para la gestión de una empresa de fabricación y venta de vehículos.

## Requisitos Previos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## Instalación

1. Clonar el repositorio (si no lo has descargado directamente):
```bash
git clone [https://github.com/JosiasmDev/erp_empresa.git]
cd erp_empresa
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear un superusuario:
```bash
python manage.py createsuperuser
```

## Configuración Inicial

1. Ejecutar el script de reset para limpiar la base de datos:
```bash
python reset.py
```

Este script creará:
- Coches (Arrow y Eclipse)
- Componentes
- Stock inicial
- Usuarios y grupos
- Empleados
- Datos de ejemplo

## Iniciar el Sistema

1. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

2. En una nueva terminal, iniciar el script de transacciones automáticas:
```bash
python auto_transactions.py
```

## Acceso al Sistema

- URL: http://127.0.0.1:8000
- Credenciales de superusuario: Las que hayas creado en el paso 5 de instalación
- Usuario de prueba: Josias (creado automáticamente)

## Estructura del Proyecto

- `erp_empresa/`: Configuración principal del proyecto
- `ecommerce/`: Módulo de comercio electrónico
- `inventory/`: Gestión de inventario
- `manufacturing/`: Gestión de producción
- `sales/`: Gestión de ventas
- `human_resources/`: Gestión de recursos humanos
- `accounting/`: Gestión contable
- `crm/`: Gestión de relaciones con clientes
- `website/`: Sitio web público

## Scripts Importantes

- `reset.py`: Limpia la base de datos y elimina todos los datos
- `create_initial_data.py`: Crea datos iniciales para el sistema
- `auto_transactions.py`: Genera transacciones automáticas (compras cada 30 segundos y sueldos cada minuto)

## Mantenimiento

Para reiniciar el sistema desde cero:
1. Detener el servidor y el script de transacciones
2. Ejecutar `python reset.py`
3. Reiniciar el servidor y el script de transacciones

## Notas Importantes

- El script `auto_transactions.py` genera compras aleatorias cada 30 segundos
- Los sueldos se pagan automáticamente cada minuto
- Asegúrate de tener suficiente espacio en disco para la base de datos
- Se recomienda hacer copias de seguridad antes de ejecutar reset.py
