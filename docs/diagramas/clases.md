# Diagrama de Clases - Sistema ERP

```mermaid
classDiagram
    %% Clases Principales
    class Usuario {
        -id: int
        -username: string
        -email: string
        -password: string
        -rol: string
        +login()
        +logout()
        +cambiarPassword()
    }

    class Cliente {
        -id: int
        -nombre: string
        -email: string
        -telefono: string
        -direccion: string
        +crearPedido()
        +verHistorial()
        +actualizarDatos()
    }

    class Pedido {
        -id: int
        -fecha: datetime
        -estado: string
        -total: decimal
        -cliente_id: int
        +calcularTotal()
        +actualizarEstado()
        +generarFactura()
    }

    class Producto {
        -id: int
        -nombre: string
        -descripcion: string
        -precio: decimal
        -stock: int
        +actualizarStock()
        +calcularPrecio()
        +verificarStock()
    }

    class OrdenFabricacion {
        -id: int
        -fecha: datetime
        -estado: string
        -pedido_id: int
        +iniciarProduccion()
        +actualizarProgreso()
        +completarOrden()
    }

    class Balance {
        -id: int
        -fecha: datetime
        -tipo: string
        -monto: decimal
        -descripcion: string
        +registrarTransaccion()
        +generarReporte()
        +calcularBalance()
    }

    class Empleado {
        -id: int
        -nombre: string
        -cargo: string
        -salario: decimal
        -departamento: string
        +registrarAsistencia()
        +calcularSalario()
        +solicitarVacaciones()
    }

    %% Relaciones
    Usuario "1" -- "*" Pedido : gestiona
    Cliente "1" -- "*" Pedido : realiza
    Pedido "*" -- "*" Producto : contiene
    Pedido "1" -- "1" OrdenFabricacion : genera
    OrdenFabricacion "*" -- "*" Producto : produce
    Balance "*" -- "1" Pedido : registra
    Empleado "*" -- "1" OrdenFabricacion : trabaja

    %% Estilos
    classDef class fill:#f9f,stroke:#333,stroke-width:2px;
    class Usuario,Cliente,Pedido,Producto,OrdenFabricacion,Balance,Empleado class;
```

## Descripción de Clases

### Usuario
- Representa los usuarios del sistema
- Gestiona la autenticación y autorización
- Maneja diferentes roles y permisos

### Cliente
- Almacena información de clientes
- Gestiona pedidos y transacciones
- Mantiene historial de compras

### Pedido
- Representa órdenes de compra
- Calcula totales y gestiona estados
- Genera facturas

### Producto
- Gestiona el catálogo de productos
- Controla inventario y precios
- Verifica disponibilidad

### OrdenFabricacion
- Controla el proceso de producción
- Gestiona recursos y personal
- Seguimiento de progreso

### Balance
- Registra transacciones contables
- Genera reportes financieros
- Calcula balances

### Empleado
- Gestiona información del personal
- Controla asistencia y salarios
- Maneja vacaciones y permisos 