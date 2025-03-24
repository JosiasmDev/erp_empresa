# Sistema ERP Empresa.

Sistema de Planificación de Recursos Empresariales (ERP) desarrollado con Django.

## Estructura del Proyecto

```
erp_empresa/
├── apps/
│   ├── sales/
│   ├── inventory/
│   ├── production/
│   ├── accounting/
│   ├── human_resources/
│   └── marketing/
├── docs/
│   ├── diagramas/
│   │   ├── casos_uso.md
│   │   ├── clases.md
│   │   ├── der.md
│   │   ├── secuencia_venta.md
│   │   ├── estados_pedido.md
│   │   ├── componentes.md
│   │   └── despliegue.md
│   ├── documentacion_tecnica.md
│   └── documentacion_funcional.md
└── requirements.txt
```

## Requisitos

- Python 3.8+
- Django 4.2+
- PostgreSQL
- Redis
- RabbitMQ

## Instalación

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

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Migrar base de datos:
```bash
python manage.py migrate
```

## Visualización de Diagramas

Los diagramas están creados usando Mermaid y se encuentran en la carpeta `docs/diagramas/`. Para visualizarlos:

1. **Usando GitHub**: 
   - Los archivos .md con diagramas Mermaid se renderizan automáticamente en GitHub
   - Navega a la carpeta `docs/diagramas/` en el repositorio
   - Abre cualquier archivo .md para ver el diagrama

2. **Usando VS Code**:
   - Instala la extensión "Markdown Preview Mermaid Support"
   - Abre el archivo .md
   - Presiona Ctrl+Shift+V (o Cmd+Shift+V en Mac) para ver la vista previa

3. **Usando Mermaid Live Editor**:
   - Ve a https://mermaid.live
   - Copia el contenido del diagrama (código entre ```mermaid)
   - Pega en el editor para visualizar

## Documentación

- **Documentación Técnica**: `docs/documentacion_tecnica.md`
  - Arquitectura del sistema
  - Configuración técnica
  - Guías de desarrollo

- **Documentación Funcional**: `docs/documentacion_funcional.md`
  - Manual de usuario
  - Casos de uso
  - Requisitos de seguridad
  - Preguntas frecuentes

## Diagramas Disponibles

1. **Casos de Uso** (`casos_uso.md`)
   - Muestra los actores y funcionalidades del sistema

2. **Diagrama de Clases** (`clases.md`)
   - Representa la estructura de clases del sistema

3. **Diagrama Entidad-Relación** (`der.md`)
   - Muestra el modelo de datos

4. **Diagrama de Secuencia** (`secuencia_venta.md`)
   - Proceso de venta detallado

5. **Diagrama de Estados** (`estados_pedido.md`)
   - Estados y transiciones de pedidos

6. **Diagrama de Componentes** (`componentes.md`)
   - Arquitectura del sistema

7. **Diagrama de Despliegue** (`despliegue.md`)
   - Infraestructura de producción

## Desarrollo

Para ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

Para ejecutar las tareas programadas:
```bash
python ejecutar_tareas_script.py
```

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
