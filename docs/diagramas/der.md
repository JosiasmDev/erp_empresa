# Diagrama Entidad-Relación (DER) - Sistema ERP

```mermaid
erDiagram
    USUARIO ||--o{ PEDIDO : gestiona
    CLIENTE ||--o{ PEDIDO : realiza
    PEDIDO ||--|{ DETALLE_PEDIDO : tiene
    DETALLE_PEDIDO }|--|| PRODUCTO : incluye
    PEDIDO ||--|| ORDEN_FABRICACION : genera
    ORDEN_FABRICACION ||--|{ DETALLE_FABRICACION : contiene
    DETALLE_FABRICACION }|--|| PRODUCTO : utiliza
    EMPLEADO ||--o{ ORDEN_FABRICACION : trabaja_en
    BALANCE ||--o{ TRANSACCION : registra
    TRANSACCION }|--|| PEDIDO : corresponde

    USUARIO {
        string username PK
        string email
        string password
        string rol
        boolean activo
    }

    CLIENTE {
        string id PK
        string nombre
        string direccion
        string telefono
        string email
        string nif
    }

    PEDIDO {
        string numero PK
        date fecha
        float total
        string estado
        string cliente_id FK
    }

    PRODUCTO {
        string codigo PK
        string nombre
        float precio
        integer stock
        string categoria
    }

    ORDEN_FABRICACION {
        string numero PK
        date fecha_inicio
        date fecha_fin
        string estado
        string pedido_id FK
    }

    DETALLE_PEDIDO {
        integer id PK
        string pedido_id FK
        string producto_id FK
        integer cantidad
        float precio_unitario
    }

    DETALLE_FABRICACION {
        integer id PK
        string orden_id FK
        string producto_id FK
        integer cantidad
        string estado
    }

    EMPLEADO {
        string id PK
        string nombre
        string cargo
        float salario
        date fecha_ingreso
    }

    BALANCE {
        integer id PK
        date fecha
        float saldo_actual
    }

    TRANSACCION {
        integer id PK
        integer balance_id FK
        string pedido_id FK
        date fecha
        float monto
        string tipo
    }
```

## Descripción de Entidades y Relaciones

### Entidades Principales

#### USUARIO
- Almacena información de usuarios del sistema
- Clave primaria: id
- Relacionada con PEDIDO (1:N)

#### CLIENTE
- Gestiona información de clientes
- Clave primaria: id
- Relacionada con PEDIDO (1:N)

#### PEDIDO
- Registra órdenes de compra
- Clave primaria: id
- Claves foráneas: cliente_id, usuario_id
- Relacionada con DETALLE_PEDIDO (1:N)

#### PRODUCTO
- Gestiona el catálogo de productos
- Clave primaria: id
- Relacionada con DETALLE_PEDIDO (1:N)

#### ORDEN_FABRICACION
- Controla órdenes de producción
- Clave primaria: id
- Clave foránea: pedido_id
- Relacionada con DETALLE_FABRICACION (1:N)

#### EMPLEADO
- Gestiona información del personal
- Clave primaria: id
- Relacionada con ORDEN_FABRICACION (1:N)

#### BALANCE
- Registra transacciones contables
- Clave primaria: id
- Clave foránea: pedido_id
- Relacionada con TRANSACCION (1:N)

### Entidades de Detalle

#### DETALLE_PEDIDO
- Registra productos en cada pedido
- Clave primaria: id
- Claves foráneas: pedido_id, producto_id

#### DETALLE_FABRICACION
- Controla detalles de producción
- Clave primaria: id
- Claves foráneas: orden_id, producto_id

#### TRANSACCION
- Registra movimientos contables
- Clave primaria: id
- Clave foránea: balance_id

### Relaciones
1. Un usuario puede gestionar varios pedidos
2. Un cliente puede realizar varios pedidos
3. Un pedido puede contener varios productos
4. Una orden de fabricación puede producir varios productos
5. Un empleado puede trabajar en varias órdenes de fabricación
6. Un balance puede contener varias transacciones 