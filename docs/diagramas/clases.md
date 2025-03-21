# Diagrama de Clases - Sistema ERP

```mermaid
classDiagram
    class Usuario {
        +String username
        +String email
        +String password
        +String rol
        +Boolean is_active
        +autenticar()
        +cambiarPassword()
        +gestionarPermisos()
    }

    class Cliente {
        +String nombre
        +String direccion
        +String telefono
        +String email
        +String nif
        +crearPedido()
        +actualizarDatos()
        +verHistorial()
    }

    class Pedido {
        +String numero
        +Date fecha
        +Float total
        +String estado
        +calcularTotal()
        +generarFactura()
        +actualizarEstado()
    }

    class Producto {
        +String codigo
        +String nombre
        +Float precio
        +Int stock
        +String categoria
        +actualizarStock()
        +calcularPrecio()
        +verificarDisponibilidad()
    }

    class OrdenFabricacion {
        +String numero
        +Date fecha_inicio
        +Date fecha_fin
        +String estado
        +planificarProduccion()
        +asignarRecursos()
        +actualizarEstado()
    }

    class Balance {
        +Date fecha
        +Float monto
        +String tipo
        +String descripcion
        +registrarMovimiento()
        +calcularSaldo()
        +generarInforme()
    }

    class Empleado {
        +String nombre
        +String cargo
        +Float salario
        +Date fecha_ingreso
        +registrarAsistencia()
        +calcularSalario()
        +evaluarDesempeño()
    }

    Usuario "1" --> "*" Pedido : gestiona
    Cliente "1" --> "*" Pedido : crea
    Pedido "*" --> "*" Producto : contiene
    Pedido "1" --> "1" OrdenFabricacion : genera
    OrdenFabricacion "*" --> "*" Producto : produce
    Balance "1" --> "*" Pedido : registra
    Empleado "1" --> "*" OrdenFabricacion : trabaja

    note "Sistema ERP - Diagrama de Clases"
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