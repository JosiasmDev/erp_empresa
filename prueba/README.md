# ERP Empresa - Sistema de Gestión Empresarial

## Descripción
ERP Empresa es un sistema de gestión empresarial desarrollado con Django que integra múltiples módulos para la gestión completa de una empresa. El sistema está diseñado siguiendo los principios de Métrica 3 y las mejores prácticas de desarrollo de software.

## Características Principales
- Gestión de Inventario
- Ventas y CRM
- Contabilidad
- Recursos Humanos
- Manufactura
- E-commerce
- Marketing Automation

## Requisitos del Sistema
- Python 3.12+
- PostgreSQL 14+
- Django 4.2
- Dependencias listadas en requirements.txt

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd erp_empresa
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con las configuraciones necesarias
```

5. Realizar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Iniciar el servidor:
```bash
python manage.py runserver
```

## Estructura del Proyecto
```
erp_empresa/
├── accounts/          # Gestión de usuarios y autenticación
├── accounting/        # Módulo de contabilidad
├── crm/              # Gestión de relaciones con clientes
├── ecommerce/        # Tienda en línea
├── human_resources/  # Gestión de recursos humanos
├── inventory/        # Control de inventario
├── manufacturing/    # Gestión de producción
├── marketing_automation/  # Automatización de marketing
├── purchase/         # Gestión de compras
├── sales/           # Gestión de ventas
└── website/         # Sitio web público
```

## Documentación
Para una documentación detallada, consultar:
- [Documentación Técnica](documentacion/tecnica.md)
- [Manual de Usuario](documentacion/usuario.md)
- [Diagramas del Sistema](documentacion/diagramas.md)

## Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles. 