# Documentación Técnica - ERP Empresa

## 1. Requisitos del Proyecto

### Objetivo del Proyecto
Desarrollar un sistema ERP completo que integre todas las áreas funcionales de una empresa, proporcionando una solución unificada para la gestión empresarial.

### Alcance y Funcionalidades Principales
- Gestión de Inventario
  - Control de stock
  - Movimientos de inventario
  - Alertas de stock mínimo
  - Gestión de componentes

- Ventas y CRM
  - Gestión de pedidos
  - Seguimiento de clientes
  - Historial de ventas
  - Gestión de cotizaciones

- Contabilidad
  - Facturación
  - Gestión de pagos
  - Balance general
  - Estado de resultados

- Recursos Humanos
  - Gestión de empleados
  - Control de sueldos
  - Gestión de permisos
  - Evaluaciones

- Manufactura
  - Órdenes de producción
  - Control de calidad
  - Gestión de componentes
  - Planificación de producción

- E-commerce
  - Catálogo de productos
  - Carrito de compras
  - Proceso de pago
  - Gestión de pedidos online

### Tecnologías Utilizadas
- Backend:
  - Django 4.2
  - PostgreSQL 14
  - Redis (caché)
  - Celery (tareas asíncronas)

- Frontend:
  - Bootstrap 5
  - jQuery
  - Chart.js (gráficos)

- Herramientas de Desarrollo:
  - Git
  - Docker
  - GitHub Actions (CI/CD)

### Requisitos del Sistema
- Hardware:
  - CPU: 4+ cores
  - RAM: 8GB+
  - Disco: 50GB+ SSD

- Software:
  - Sistema Operativo: Windows 10/11, Linux, macOS
  - Python 3.12+
  - PostgreSQL 14+
  - Redis 6+

## 2. Guía de Instalación y Configuración

### Requisitos Previos
1. Python 3.12 o superior
2. PostgreSQL 14 o superior
3. Redis 6 o superior
4. Git

### Instalación del Proyecto
1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd erp_empresa
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Configuración del Entorno
1. Crear archivo .env:
```bash
cp .env.example .env
```

2. Configurar variables en .env:
```env
DEBUG=True
SECRET_KEY=tu_clave_secreta
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/erp_empresa
REDIS_URL=redis://localhost:6379/0
```

3. Configurar settings.py:
```python
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'erp_empresa',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Ejecución del Servidor
1. Realizar migraciones:
```bash
python manage.py migrate
```

2. Crear superusuario:
```bash
python manage.py createsuperuser
```

3. Iniciar servidor:
```bash
python manage.py runserver
```

## 3. Estructura del Proyecto

### Directorios Principales
```
erp_empresa/
├── accounts/          # Gestión de usuarios
├── accounting/        # Contabilidad
├── crm/              # CRM
├── ecommerce/        # E-commerce
├── human_resources/  # RRHH
├── inventory/        # Inventario
├── manufacturing/    # Manufactura
├── marketing_automation/  # Marketing
├── purchase/         # Compras
├── sales/           # Ventas
└── website/         # Sitio web
```

### Arquitectura del Software
- Patrón MVC (Model-View-Controller)
- Django REST Framework para APIs
- Celery para tareas asíncronas
- Redis para caché
- PostgreSQL para base de datos

## 4. Base de Datos y Modelos

### Diagrama Entidad-Relación
[Incluir diagrama ERD]

### Modelos Principales
1. Usuario y Autenticación
```python
class User(AbstractUser):
    # Campos personalizados
    pass
```

2. Inventario
```python
class Componente(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
```

3. Ventas
```python
class Pedido(models.Model):
    numero_pedido = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
```

## 5. APIs y Endpoints

### Autenticación
```python
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

urlpatterns = [
    path('api/token/', ObtainAuthToken.as_view(), name='api_token_auth'),
]
```

### Endpoints Principales
1. Inventario
- GET /api/inventory/componentes/
- POST /api/inventory/componentes/
- GET /api/inventory/stock/
- POST /api/inventory/movimientos/

2. Ventas
- GET /api/sales/pedidos/
- POST /api/sales/pedidos/
- GET /api/sales/clientes/
- POST /api/sales/clientes/

## 6. Manejo de Errores y Logs

### Configuración de Logging
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### Manejo de Errores
```python
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def handle_exception(exc):
    if isinstance(exc, ValidationError):
        return JsonResponse({'error': str(exc)}, status=400)
    return JsonResponse({'error': 'Error interno del servidor'}, status=500)
```

## 7. Pruebas y Deployment

### Pruebas Unitarias
```python
from django.test import TestCase

class ComponenteTests(TestCase):
    def setUp(self):
        self.componente = Componente.objects.create(
            nombre='Test Componente',
            tipo='test',
            precio_venta=100.00
        )

    def test_creacion_componente(self):
        self.assertEqual(self.componente.nombre, 'Test Componente')
        self.assertEqual(self.componente.precio_venta, 100.00)
```

### Deployment con Docker
1. Dockerfile:
```dockerfile
FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

2. docker-compose.yml:
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: erp_empresa
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: contraseña

  redis:
    image: redis:6
``` 