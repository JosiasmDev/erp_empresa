# Diagrama de Estados - Proceso de Pedido

```mermaid
stateDiagram-v2
    state "Inicio" as [*]
    state "Fin" as [*]
    
    [*] --> Nuevo: Crear Pedido
    
    Nuevo --> EnProceso: Validar Pedido
    Nuevo --> Cancelado: Cancelar Pedido
    
    EnProceso --> EnProduccion: Iniciar Producción
    EnProceso --> Cancelado: Cancelar Pedido
    
    EnProduccion --> Fabricado: Completar Producción
    EnProduccion --> Cancelado: Cancelar Producción
    
    Fabricado --> EnviadoAlmacen: Enviar a Almacén
    
    EnviadoAlmacen --> ListoParaEnvio: Preparar Envío
    
    ListoParaEnvio --> EnTransito: Iniciar Envío
    
    EnTransito --> Entregado: Confirmar Entrega
    EnTransito --> Devuelto: Rechazar Entrega
    
    Entregado --> [*]
    Cancelado --> [*]
    Devuelto --> [*]

    note right of Nuevo: Se crea el pedido<br/>con datos básicos
    note right of EnProceso: Validación de<br/>stock y recursos
    note right of EnProduccion: Fabricación de<br/>productos solicitados
    note right of Fabricado: Productos terminados<br/>y verificados
    note right of EnviadoAlmacen: En almacén para<br/>preparación
    note right of ListoParaEnvio: Empaquetado y<br/>listo para envío
    note right of EnTransito: En proceso<br/>de entrega
    note right of Entregado: Pedido entregado<br/>y confirmado

    %% Estilos de estados
    classDef default fill:#f9f,stroke:#333,stroke-width:2px
    classDef success fill:#9f9,stroke:#333,stroke-width:2px
    classDef danger fill:#f99,stroke:#333,stroke-width:2px
    
    class Entregado success
    class Cancelado,Devuelto danger
```

## Descripción del Flujo de Estados

### Estados Iniciales
- **Nuevo**: Estado inicial cuando se crea un nuevo pedido
- **EnProceso**: Validación inicial del pedido

### Estados de Producción
- **EnProduccion**: Fabricación activa del pedido
- **Fabricado**: Productos completados

### Estados de Logística
- **EnviadoAlmacen**: Productos en almacén
- **ListoParaEnvio**: Preparado para envío
- **EnTransito**: En proceso de entrega

### Estados Finales
- **Entregado**: Entrega exitosa
- **Cancelado**: Pedido cancelado
- **Devuelto**: Pedido devuelto

### Transiciones Principales
1. Creación → Validación
2. Validación → Producción
3. Producción → Almacén
4. Almacén → Envío
5. Envío → Entrega

### Estados de Excepción
- Cancelación en cualquier etapa
- Devolución durante el envío
``` 