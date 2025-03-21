# Diagrama de Secuencia - Proceso de Venta

```mermaid
sequenceDiagram
    participant C as Cliente
    participant V as Vendedor
    participant S as Sistema
    participant I as Inventario
    participant P as Producción
    participant F as Facturación
    participant DB as Base de Datos

    %% Inicio del proceso de venta
    C->>V: Solicita producto
    V->>S: Inicia proceso de venta
    S->>I: Verifica stock
    I-->>S: Stock disponible
    S->>DB: Crea pedido
    DB-->>S: Pedido creado

    %% Proceso de pago
    S->>F: Inicia proceso de pago
    F->>C: Solicita datos de pago
    C->>F: Proporciona datos
    F->>DB: Registra pago
    DB-->>F: Pago confirmado
    F-->>S: Pago procesado

    %% Proceso de producción
    S->>P: Crea orden de fabricación
    P->>DB: Registra orden
    DB-->>P: Orden registrada
    P->>I: Reserva materiales
    I-->>P: Materiales reservados
    P-->>S: Orden iniciada

    %% Actualización de inventario
    P->>I: Actualiza stock
    I->>DB: Registra cambios
    DB-->>I: Cambios guardados
    I-->>S: Stock actualizado

    %% Generación de factura
    S->>F: Solicita factura
    F->>DB: Genera factura
    DB-->>F: Factura creada
    F->>C: Envía factura
    F-->>S: Proceso completado

    %% Notificaciones
    S->>C: Notifica estado del pedido
    S->>V: Actualiza estado de venta
    V->>C: Confirma entrega

    %% Estilos
    Note over C,F: Proceso de Pago
    Note over P,I: Proceso de Producción
    Note over S,F: Proceso de Facturación
```

## Descripción del Proceso de Venta

### 1. Inicio del Proceso
1. Cliente solicita producto al vendedor
2. Vendedor inicia el proceso en el sistema
3. Sistema verifica disponibilidad de stock
4. Se crea el pedido en la base de datos

### 2. Proceso de Pago
1. Sistema inicia el proceso de pago
2. Se solicitan datos de pago al cliente
3. Se procesa el pago
4. Se registra la transacción

### 3. Proceso de Producción
1. Sistema crea orden de fabricación
2. Se registra en la base de datos
3. Se reservan materiales
4. Se inicia la producción

### 4. Actualización de Inventario
1. Se actualiza el stock
2. Se registran los cambios
3. Se confirma la actualización

### 5. Facturación
1. Sistema solicita generación de factura
2. Se crea en la base de datos
3. Se envía al cliente
4. Se completa el proceso

### 6. Notificaciones
1. Cliente recibe actualización de estado
2. Vendedor actualiza información
3. Se confirma la entrega 