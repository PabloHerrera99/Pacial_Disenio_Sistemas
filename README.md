# README.md — Sistema de Pedidos de Comida
> Proyecto académico — Aplicación de patrones **Singleton**, **Factory**, **Observer** y **Strategy**

---

## 🧩 Introducción

**PythonPedidos** es un sistema simplificado de gestión de pedidos de comida, pensado como ejercicio de diseño de software para demostrar la aplicación combinada de los **cuatro patrones de diseño clásicos**:

- **Singleton** — control central de eventos (`OrderManager`).
- **Factory Method** — creación de pedidos, pagos y notificaciones.
- **Observer** — sistema de eventos y listeners que reaccionan en tiempo real.
- **Strategy** — variación de comportamientos en envíos y asignación de repartidores.

El proyecto reproduce el flujo típico de un sistema de pedidos:  
> Crear pedido → Pagar → Preparar (en tiempo real) → Asignar repartidor → Entregar.

Incluye simulación de progreso, notificaciones y auditoría de eventos en disco.

---

## 🏗️ Arquitectura del sistema

```
PythonPedidos/
│
├── main.py                         # Punto de entrada del sistema
├── README.md                       # Este archivo
├── USER_STORIES.md                 # Historias de usuario detalladas
├── RUBRICA_EVALUACION.md           # Rúbrica técnica (si aplica)
│
├── data/                           # Persistencia de eventos (events.dat JSONL)
│
└── python_pedidos/
    ├── __init__.py
    ├── constantes.py                # Constantes globales
    │
    ├── core/                        # Núcleo de eventos y observadores
    │   ├── events.py                # Definición de eventos
    │   ├── observers.py             # Interfaz Observer
    │   ├── order_manager.py         # Singleton + dispatcher de eventos
    │   └── listeners.py             # Observers concretos (Dashboard, Auditoría, Log, Cocina)
    │
    ├── entidades/                   # Dominio del negocio
    │   ├── menu.py                  # Ítems del menú
    │   ├── pedido.py                # Pedido con ítems y total
    │   └── pago.py                  # Pago y estados
    │
    ├── factories/                   # Fabricación de objetos (Factory Method)
    │   ├── pedido_factory.py
    │   ├── pago_factory.py
    │   └── notificacion_factory.py
    │
    ├── patrones/                    # Implementaciones de patrones
    │   └── strategy/
    │       ├── envio_strategy.py    # Envío (Rápido, Económico, Ecológico)
    │       └── asignacion_strategy.py # Asignación de repartidores
    │
    └── servicios/                   # Lógica de negocio
        ├── pedido_service.py        # Orquestador del flujo de pedido
        ├── pago_service.py          # Pago y validación
        ├── cocina_service.py        # Preparación (utilizado por Observer)
        └── reparto_service.py       # Asignación de delivery
```

---

## ⚙️ Patrones implementados

| Patrón | Archivo / Clase Principal | Rol |
|--------|----------------------------|-----|
| **Singleton** | `core/order_manager.py` (`OrderManager`) | Controla los eventos globales y el log central del sistema. |
| **Factory Method** | `factories/pedido_factory.py`, `pago_factory.py`, `notificacion_factory.py` | Permite crear instancias de pedidos, pagos o notificadores según el tipo solicitado. |
| **Observer** | `core/listeners.py`, `core/order_manager.py` | Gestiona la suscripción y notificación automática ante eventos del negocio. |
| **Strategy** | `patrones/strategy/envio_strategy.py`, `asignacion_strategy.py` | Define estrategias intercambiables de cálculo de envío y asignación de repartidores. |

---

## 🧠 Flujo de ejecución (demo)

1. **Creación del pedido:**  
   Se usa `PedidoFactory` para generar un pedido Delivery o Retiro con ítems y cálculo de total.

2. **Pago del pedido:**  
   `PagoService` valida el método de pago (tarjeta, transferencia, etc.)  
   Si el pago se aprueba → se dispara evento `PagoAprobado`.

3. **Preparación (Observer en tiempo real):**  
   `CocinaRealtimeListener` detecta `PagoAprobado` y lanza un hilo que publica:
   - `PreparacionIniciada`
   - `PreparacionAvance` (0% → 100%)
   - `PedidoListo`

4. **Asignación de delivery (Strategy):**  
   `RepartoService` utiliza la estrategia seleccionada (`AsignacionCercano` o `AsignacionBalanceada`) para elegir un repartidor.  
   Se publican `DeliveryAsignado` y `SalioAReparto`.

5. **Entrega:**  
   Cuando el pedido llega al cliente, se ejecuta `PedidoEntregado` y se cierra el flujo.

---

## 🖥️ Ejecución de la demo

1. Asegurate de tener **Python 3.10+** instalado.  
2. Parate en la carpeta raíz del proyecto (la que contiene `python_pedidos/`).  
3. Ejecutá el sistema con:

```bash
python -m python_pedidos.app
# o
python main.py
```

### Salida esperada
- La consola mostrará iconos por cada evento (`🛒`, `💳`, `👨‍🍳`, `⏳`, `🛵`, `🎉`, etc.).  
- Durante la preparación verás una **barra de progreso** simulando el avance en cocina.  
- Se generará un archivo `data/events.dat` con los eventos registrados en formato JSONL.

---

## 🧾 Ejemplo de salida

```
[DASH] 🛒 PedidoCreado :: {'pedido_id': 'P-RT-001', 'total': 8700.0}
[DASH] 💳✅ PagoAprobado :: {'pedido_id': 'P-RT-001', 'monto': 8700.0, 'metodo': 'Tarjeta'}
[DASH] 👨‍🍳 PreparacionIniciada :: {'pedido_id': 'P-RT-001'}
[DASH] ⏳ Prep  25% [██░░░░░░░] (step=2)
[DASH] ✅🍽️ PedidoListo :: {'pedido_id': 'P-RT-001'}
[DASH] 🛵 DeliveryAsignado :: {'pedido_id': 'P-RT-001', 'repartidor': 'Mica'}
[DASH] ➡️🛵 SalioAReparto :: {'pedido_id': 'P-RT-001', 'repartidor': 'Mica'}
[DASH] 🎉📦 PedidoEntregado :: {'pedido_id': 'P-RT-001'}
```

---

## 📊 Persistencia y auditoría

Cada evento se guarda automáticamente en:
```
data/events.dat
```
Formato JSONL (una línea por evento):
```json
{"ts": "2025-10-28T14:12:31Z", "tipo": "PagoAprobado", "payload": {"pedido_id": "P-RT-001", "monto": 8700.0}}
```

Si ocurre un error de escritura, se muestra en consola con `[AUDIT][ERROR]` pero no detiene el sistema.

---

## 🧱 Extensibilidad

- **Nuevas estrategias de envío:** crear clase que implemente `EnvioStrategy` y registrarla en `PedidoFactory`.
- **Nuevos métodos de pago:** extender `PagoFactory`.
- **Nuevos tipos de notificación:** implementar `Notificador` y agregar en `NotificacionFactory`.
- **Nuevas estrategias de asignación:** crear clase hija de `AsignacionStrategy` y usar `set_strategy()`.


---

## ✅ Definition of Done (resumen)

- Demo ejecutable y observable en consola.  
- Eventos persistidos (`data/events.dat`).  
- Diagramas actualizados.  
- Historias de usuario trazadas.  
- README y rúbricas completas.


