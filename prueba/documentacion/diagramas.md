# Diagramas del Sistema - ERP Empresa

## 1. Modelo de Análisis (MA)

### 1.1 Diagrama de Casos de Uso
```mermaid
graph TD
    A[Usuario] --> B[Gestión de Inventario]
    A --> C[Ventas y CRM]
    A --> D[Contabilidad]
    A --> E[Recursos Humanos]
    A --> F[Manufactura]
    A --> G[E-commerce]
    
    B --> B1[Ver Stock]
    B --> B2[Registrar Movimientos]
    B --> B3[Alertas de Stock]
    
    C --> C1[Crear Pedidos]
    C --> C2[Gestionar Clientes]
    C --> C3[Historial de Ventas]
    
    D --> D1[Facturación]
    D --> D2[Balance General]
    D --> D3[Estado de Resultados]
    
    E --> E1[Gestión de Empleados]
    E --> E2[Control de Sueldos]
    E --> E3[Evaluaciones]
    
    F --> F1[Órdenes de Producción]
    F --> F2[Control de Calidad]
    F --> F3[Planificación]
    
    G --> G1[Catálogo de Productos]
    G --> G2[Pedidos Online]
    G --> G3[Proceso de Pago]
```

### 1.2 Diagrama de Clases
```mermaid
classDiagram
    class Usuario {
        +String username
        +String email
        +String password
        +Boolean is_active
        +crear_usuario()
        +cambiar_password()
    }
    
    class Cliente {
        +String nombre
        +String email
        +String telefono
        +crear_cliente()
        +actualizar_datos()
    }
    
    class Producto {
        +String nombre
        +String descripcion
        +Decimal precio
        +Integer stock
        +crear_producto()
        +actualizar_stock()
    }
    
    class Pedido {
        +String numero_pedido
        +Cliente cliente
        +List~Producto~ productos
        +Decimal total
        +crear_pedido()
        +calcular_total()
    }
    
    Usuario <|-- Cliente
    Pedido --> Cliente
    Pedido --> Producto
```

### 1.3 Diagrama Entidad-Relación (DER)
```mermaid
erDiagram
    USUARIO ||--o{ PEDIDO : realiza
    USUARIO {
        int id PK
        string username
        string email
        string password
        boolean is_active
    }
    
    CLIENTE ||--o{ PEDIDO : tiene
    CLIENTE {
        int id PK
        string nombre
        string email
        string telefono
    }
    
    PRODUCTO ||--o{ DETALLE_PEDIDO : contiene
    PRODUCTO {
        int id PK
        string nombre
        string descripcion
        decimal precio
        int stock
    }
    
    PEDIDO ||--o{ DETALLE_PEDIDO : tiene
    PEDIDO {
        int id PK
        int cliente_id FK
        int usuario_id FK
        date fecha
        decimal total
    }
    
    DETALLE_PEDIDO {
        int id PK
        int pedido_id FK
        int producto_id FK
        int cantidad
        decimal precio_unitario
    }
```

## 2. Modelo de Diseño (MD)

### 2.1 Diagrama de Secuencia - Proceso de Venta
```mermaid
sequenceDiagram
    participant C as Cliente
    participant V as Vendedor
    participant S as Sistema
    participant I as Inventario
    
    C->>V: Solicita producto
    V->>S: Verifica stock
    S->>I: Consulta disponibilidad
    I-->>S: Confirma stock
    S-->>V: Muestra disponibilidad
    V->>S: Crea pedido
    S->>I: Reserva stock
    I-->>S: Confirma reserva
    S-->>V: Genera pedido
    V-->>C: Entrega pedido
```

### 2.2 Diagrama de Estados - Pedido
```mermaid
stateDiagram-v2
    [*] --> Pendiente
    Pendiente --> En_Proceso
    En_Proceso --> Completado
    En_Proceso --> Cancelado
    Completado --> [*]
    Cancelado --> [*]
```

## 3. Especificación de Construcción (EC)

### 3.1 Diagrama de Componentes
```mermaid
graph TD
    A[Frontend] --> B[Backend]
    B --> C[Base de Datos]
    B --> D[Cache]
    
    A --> A1[HTML/CSS]
    A --> A2[JavaScript]
    A --> A3[Bootstrap]
    
    B --> B1[Django]
    B --> B2[DRF]
    B --> B3[Celery]
    
    C --> C1[PostgreSQL]
    D --> D1[Redis]
```

### 3.2 Diagrama de Despliegue
```mermaid
graph TD
    A[Cliente Web] --> B[Load Balancer]
    B --> C1[Servidor Web 1]
    B --> C2[Servidor Web 2]
    
    C1 --> D[Base de Datos]
    C2 --> D
    
    C1 --> E[Cache Redis]
    C2 --> E
    
    C1 --> F[Almacenamiento]
    C2 --> F
```

## 4. Flujos de Proceso

### 4.1 Proceso de Fabricación
```mermaid
graph LR
    A[Crear Orden] --> B[Asignar Componentes]
    B --> C[Iniciar Producción]
    C --> D[Control de Calidad]
    D --> E[Almacenar]
    E --> F[Entregar]
```

### 4.2 Proceso de Compra
```mermaid
graph LR
    A[Crear Orden] --> B[Aprobar Compra]
    B --> C[Recibir Productos]
    C --> D[Control de Calidad]
    D --> E[Registrar Pago]
    E --> F[Actualizar Inventario]
```

## 5. Arquitectura de Datos

### 5.1 Modelo de Datos Principal
```mermaid
erDiagram
    EMPLEADO ||--o{ SUELDO : recibe
    EMPLEADO {
        int id PK
        string nombre
        string cargo
        decimal sueldo_base
    }
    
    SUELDO {
        int id PK
        int empleado_id FK
        decimal monto
        date fecha
        boolean pagado
    }
    
    COMPONENTE ||--o{ STOCK : tiene
    COMPONENTE {
        int id PK
        string nombre
        string tipo
        decimal precio_venta
    }
    
    STOCK {
        int id PK
        int componente_id FK
        int cantidad
        string ubicacion
    }
    
    PEDIDO ||--o{ ORDEN_FABRICACION : genera
    PEDIDO {
        int id PK
        int cliente_id FK
        date fecha
        string estado
    }
    
    ORDEN_FABRICACION {
        int id PK
        int pedido_id FK
        date fecha_inicio
        date fecha_fin
        string estado
    }
```

### 5.2 Modelo de Datos de Contabilidad
```mermaid
erDiagram
    CUENTA ||--o{ TRANSACCION : tiene
    CUENTA {
        int id PK
        string nombre
        string tipo
        decimal saldo
    }
    
    TRANSACCION {
        int id PK
        int cuenta_id FK
        decimal monto
        date fecha
        string tipo
    }
    
    FACTURA ||--o{ TRANSACCION : genera
    FACTURA {
        int id PK
        int pedido_id FK
        date fecha
        decimal total
    }
``` 