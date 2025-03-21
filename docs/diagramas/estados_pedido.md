# Diagrama de Estados - Proceso de Pedido

```mermaid
stateDiagram-v2
    [*] --> Pendiente: Crear pedido
    
    state Pendiente {
        [*] --> ValidandoStock
        ValidandoStock --> StockDisponible: Stock OK
        ValidandoStock --> SinStock: Sin stock
        StockDisponible --> EsperandoPago
        SinStock --> [*]
    }
    
    Pendiente --> EsperandoPago: Validación exitosa
    EsperandoPago --> PagoProcesado: Pago confirmado
    EsperandoPago --> Cancelado: Pago fallido
    
    PagoProcesado --> EnProduccion: Crear orden de fabricación
    EnProduccion --> EnFabricacion: Iniciar producción
    EnFabricacion --> ControlCalidad: Producción completada
    ControlCalidad --> Aprobado: Pasa control
    ControlCalidad --> Rechazado: No pasa control
    Rechazado --> EnFabricacion: Rehacer
    
    Aprobado --> EnAlmacen: Almacenar
    EnAlmacen --> Enviado: Preparar envío
    Enviado --> Entregado: Confirmar entrega
    
    Cancelado --> [*]
    Entregado --> [*]
    
    %% Estilos
    classDef state fill:#f9f,stroke:#333,stroke-width:2px;
    classDef final fill:#fdd,stroke:#333,stroke-width:2px;
    classDef initial fill:#dfd,stroke:#333,stroke-width:2px;
    
    class Pendiente,EsperandoPago,PagoProcesado,EnProduccion,EnFabricacion,ControlCalidad,Aprobado,Rechazado,EnAlmacen,Enviado state;
    class Cancelado,Entregado final;
    class [*] initial;
```

## Descripción de Estados del Pedido

### 1. Estado Inicial
- **Pendiente**
  - Pedido recién creado
  - Validación inicial de datos
  - Verificación de stock

### 2. Proceso de Pago
- **EsperandoPago**
  - Cliente debe realizar el pago
  - Sistema espera confirmación
  - Tiempo límite de pago

- **PagoProcesado**
  - Pago confirmado
  - Transacción registrada
  - Listo para producción

### 3. Proceso de Producción
- **EnProduccion**
  - Orden de fabricación creada
  - Asignación de recursos
  - Planificación de producción

- **EnFabricacion**
  - Producción en curso
  - Seguimiento de progreso
  - Control de materiales

- **ControlCalidad**
  - Verificación de calidad
  - Pruebas de funcionamiento
  - Documentación técnica

### 4. Estados de Control
- **Aprobado**
  - Pasa control de calidad
  - Cumple especificaciones
  - Listo para almacenamiento

- **Rechazado**
  - No cumple especificaciones
  - Requiere correcciones
  - Vuelve a fabricación

### 5. Proceso de Entrega
- **EnAlmacen**
  - Producto almacenado
  - Preparación para envío
  - Control de inventario

- **Enviado**
  - En proceso de envío
  - Seguimiento de entrega
  - Notificaciones al cliente

### 6. Estados Finales
- **Entregado**
  - Pedido completado
  - Cliente confirma recepción
  - Documentación finalizada

- **Cancelado**
  - Pedido anulado
  - Razón de cancelación
  - Registro de incidencia

### Transiciones Importantes
1. Pendiente → EsperandoPago: Validación exitosa
2. EsperandoPago → PagoProcesado: Pago confirmado
3. PagoProcesado → EnProduccion: Crear orden
4. EnFabricacion → ControlCalidad: Producción lista
5. ControlCalidad → Aprobado/Rechazado: Resultado control
6. Aprobado → EnAlmacen: Almacenamiento
7. EnAlmacen → Enviado: Preparación envío
8. Enviado → Entregado: Confirmación cliente 