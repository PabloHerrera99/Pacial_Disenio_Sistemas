# USER_STORIES.md — Sistema de Pedidos de Comida
> Proyecto: **PythonPedidos** — Patrones: *Singleton, Factory, Observer, Strategy*

Formato: **Como [Actor] quiero [Funcionalidad] para [Beneficio]**  
Incluye: *Criterios de Aceptación (Gherkin), Prioridad (MoSCoW), Estimación (pts), Trazabilidad a Patrones/Clases.*

---

## HU-001 — Navegar menú y armar carrito
**Como** cliente  
**Quiero** ver el menú y agregar/quitar ítems con cantidades  
**Para** armar mi pedido

**Criterios de Aceptación**
- Dado que abro el menú, Cuando agrego un ítem con cantidad N, Entonces el carrito muestra ítem y subtotal.
- Dado un ítem en el carrito, Cuando modifico su cantidad o lo quito, Entonces el total se recalcula.
- Dado un carrito vacío, Cuando consulto el total, Entonces el total es 0.

**Prioridad:** Must • **Estimación:** 3 pts  
**Trazabilidad:** Dominio (`ItemMenu`), Servicio (`PedidoService.crear_pedido` prepara datos).

---

## HU-002 — Crear pedido (Delivery / Retiro)
**Como** cliente  
**Quiero** crear mi pedido indicando tipo y datos básicos  
**Para** iniciar el proceso de compra

**Criterios de Aceptación**
- Dado un carrito válido, Cuando creo pedido **Delivery** con dirección, Entonces queda **CREADO** con ID y total preliminar.
- Dado un carrito válido, Cuando creo pedido **Retiro**, Entonces queda **CREADO** sin dirección.
- Al crear, se publica el evento `PedidoCreado`.

**Prioridad:** Must • **Estimación:** 3 pts  
**Trazabilidad:** **Factory** (`PedidoFactory`), **Observer** (`OrderManager.publicar(PedidoCreado)`), Dominio (`Pedido`).

---

## HU-003 — Elegir estrategia de envío (Rápido/Económico/Ecológico)
**Como** cliente de delivery  
**Quiero** seleccionar la modalidad de envío  
**Para** balancear costo y tiempo

**Criterios de Aceptación**
- Dado un pedido delivery, Cuando selecciono **Rápido**, Entonces el costo usa `EnvioRapido` y se expone ETA.
- Cuando elijo **Económico** o **Ecológico**, Entonces aplica la estrategia correspondiente y el total se actualiza.

**Prioridad:** Should • **Estimación:** 3 pts  
**Trazabilidad:** **Strategy** (`EnvioStrategy` y concretas), **Factory** (traducción de string a strategy en `PedidoFactory`).

---

## HU-004 — Pagar pedido
**Como** cliente  
**Quiero** elegir método de pago (Tarjeta/Transferencia/Wallet)  
**Para** completar la compra

**Criterios de Aceptación**
- Dado un pedido **CREADO**, Cuando pago con método válido, Entonces el pago queda **APROBADO** y se publica `PagoAprobado`.
- Dado un método rechazado, Cuando intento pagar, Entonces se publica `PedidoCancelado` con motivo y el flujo se detiene.

**Prioridad:** Must • **Estimación:** 3 pts  
**Trazabilidad:** **Factory** (`PagoFactory`), **Observer** (eventos de pago), Servicios (`PagoService`).

---

## HU-005 — Preparación de cocina (progreso en tiempo real)
**Como** cocina  
**Quiero** comenzar la preparación automáticamente al aprobarse el pago  
**Para** optimizar tiempos

**Criterios de Aceptación**
- Dado `PagoAprobado`, Cuando inicia cocina, Entonces se publica `PreparacionIniciada`.
- Durante la preparación, Cuando transcurre cada tick, Entonces se publica `PreparacionAvance` con `%` (hasta 100).
- Al finalizar, Entonces se publica `PedidoListo`.

**Prioridad:** Must • **Estimación:** 5 pts  
**Trazabilidad:** **Observer** (`CocinaRealtimeListener` simula ticks), **Singleton** (`OrderManager`), Eventos (`Preparacion*`, `PedidoListo`).

---

## HU-006 — Asignación de repartidor (reglas de negocio)
**Como** operador de logística  
**Quiero** asignar repartidor usando reglas configurables  
**Para** optimizar cercanía o balance de carga

**Criterios de Aceptación**
- Dado `PedidoListo`, Cuando aplico `AsignacionCercano`, Entonces se asigna quien cubre la **misma zona** si existe.
- Dado `PedidoListo`, Cuando aplico `AsignacionBalanceada`, Entonces se asigna el de **menor carga**.
- Al asignar, se publican `DeliveryAsignado` y `SalioAReparto`.

**Prioridad:** Should • **Estimación:** 5 pts  
**Trazabilidad:** **Strategy** (`AsignacionStrategy`), **Observer** (eventos), Servicio (`RepartoService`).

---

## HU-007 — Notificaciones en cada hito
**Como** cliente  
**Quiero** recibir notificaciones en eventos clave  
**Para** seguir el estado del pedido

**Criterios de Aceptación**
- Ante `PedidoCreado`, `PagoAprobado`, `PreparacionIniciada`, `PreparacionAvance`, `PedidoListo`, `DeliveryAsignado`, `SalioAReparto`, `PedidoEntregado`, `PedidoCancelado` se dispara una notificación (Email/SMS/Push) según canal configurado.
- Cada notificación deja registro en el log del sistema.

**Prioridad:** Must • **Estimación:** 3 pts  
**Trazabilidad:** **Factory** (`NotificacionFactory`), **Observer** (`ConsoleDashboard`, `FileAuditListener`, `LogListener`).

---

## HU-008 — Entregar pedido y cerrar flujo
**Como** repartidor  
**Quiero** marcar pedido como entregado  
**Para** cerrar el ciclo

**Criterios de Aceptación**
- Dado un pedido **EN CAMINO**, Cuando marco **ENTREGADO**, Entonces se publica `PedidoEntregado` y se persiste en auditoría.
- No se puede marcar **ENTREGADO** si el pedido no llegó al estado **LISTO**.

**Prioridad:** Must • **Estimación:** 2 pts  
**Trazabilidad:** **Observer** (evento final), Servicio (`PedidoService.marcar_entregado`).

---

## HU-009 — Cancelar pedido (ventanas permitidas)
**Como** cliente u operador  
**Quiero** cancelar el pedido según reglas  
**Para** evitar costos innecesarios

**Criterios de Aceptación**
- Un pedido **CREADO** o **PAGADO** puede cancelarse si aún no está **EN PREPARACIÓN**.
- Al cancelar, se publica `PedidoCancelado` y se notifica el motivo.
- Si el pedido está **EN CAMINO**, no se permite cancelar (mensaje de política).

**Prioridad:** Should • **Estimación:** 3 pts  
**Trazabilidad:** **Observer** (evento), Servicios (política en capa de servicio).

---

## HU-010 — Persistencia de eventos (auditoría JSONL)
**Como** operador  
**Quiero** que los eventos se registren en disco  
**Para** auditoría y trazabilidad

**Criterios de Aceptación**
- Cada evento publicado se agrega a `data/events.dat` en formato **JSONL**.
- Errores de I/O son manejados con excepción controlada y mensaje `[AUDIT][ERROR]`.

**Prioridad:** Should • **Estimación:** 3 pts  
**Trazabilidad:** **Singleton** (`OrderManager` como fuente única de eventos), **Observer** (`FileAuditListener`).

---

## HU-011 — Retiro en local (sin envío)
**Como** cliente  
**Quiero** elegir **Retiro** en lugar de **Delivery**  
**Para** evitar tiempo/costo de envío

**Criterios de Aceptación**
- Dado tipo **Retiro**, Cuando confirmo, Entonces el total **no** incluye costo de envío.
- Dado `PagoAprobado`, Cuando cocina marca listo, Entonces se notifica “**Listo para retirar**”.

**Prioridad:** Could • **Estimación:** 2 pts  
**Trazabilidad:** **Factory** (tipo de pedido/fields), **Observer** (flujo).

---

## HU-012 — Panel de consola (dashboard en tiempo real)
**Como** desarrollador/evaluador  
**Quiero** ver un panel en consola con los eventos y progreso  
**Para** entender el flujo en tiempo real

**Criterios de Aceptación**
- Al correr la demo, se imprimen iconos por evento y una **barra de progreso** durante la preparación.
- Debe verse la secuencia **Creado → Pago aprobado → Preparación → Listo → Asignado/Salida → Entregado**.

**Prioridad:** Must • **Estimación:** 2 pts  
**Trazabilidad:** **Observer** (`ConsoleDashboard`), **Singleton** (`OrderManager`).

---

# Requerimientos No Funcionales (NFR)
- **NFR-01 Observabilidad:** todo evento de negocio se loguea con timestamp y payload (consola y JSONL).
- **NFR-02 Extensibilidad:** agregar métodos de pago o estrategias de envío/asignación **sin** modificar código existente (Principio O/C).
- **NFR-03 Simplicidad:** la demo corre **sin dependencias externas**.
- **NFR-04 Robustez:** errores de auditoría no rompen el flujo principal (se registran como `[AUDIT][ERROR]`).

---

# Definition of Done (DoD)
- La **demo** corre end-to-end: Crear → Pagar → Preparar (tiempo real) → Asignar/Salir → Entregar.
- **Observer** visible (dashboard y archivo `data/events.dat`).
- **Factories** operativas para Pago/Notificación/Creación de pedido.
- **Strategies** de Envío y Asignación cambiables en caliente.
- **README**/guía de ejecución y **diagramas** actualizados (cuando se pidan).
- **Trazabilidad** HU → Componentes/Patrones documentada (esta sección).

---

# Backlog sugerido (orden de implementación)
1. HU-001, HU-002, HU-003, HU-004  
2. HU-005 (tiempo real cocina), HU-007 (notificaciones), HU-012 (dashboard)  
3. HU-006 (asignación), HU-008 (entrega)  
4. HU-009 (cancelación), HU-010 (auditoría), HU-011 (retiro)
