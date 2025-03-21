# Diagrama de Estados - Proceso de Pedido

```mermaid
stateDiagram-v2
    [*] --> Nuevo
    
    Nuevo --> EnProceso: Validar
    Nuevo --> Cancelado: Cancelar
    
    EnProceso --> EnProduccion: Iniciar Producción
    EnProceso --> Cancelado: Cancelar
    
    EnProduccion --> Fabricado: Completar
    EnProduccion --> Cancelado: Cancelar
    
    Fabricado --> EnviadoAlmacen: Enviar
    
    EnviadoAlmacen --> ListoParaEnvio: Preparar
    
    ListoParaEnvio --> EnTransito: Enviar
    
    EnTransito --> Entregado: Confirmar
    EnTransito --> Devuelto: Rechazar
    
    Entregado --> [*]
    Cancelado --> [*]
    Devuelto --> [*]

    note right of Nuevo: Se crea el pedido
    note right of EnProceso: Validación de stock
    note right of EnProduccion: En fabricación
    note right of Fabricado: Productos terminados
    note right of EnviadoAlmacen: En almacén
    note right of ListoParaEnvio: Listo para envío
    note right of EnTransito: En entrega
    note right of Entregado: Entregado al cliente
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