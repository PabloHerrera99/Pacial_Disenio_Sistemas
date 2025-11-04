"""
Archivo integrador generado automaticamente
Directorio: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core
Fecha: 2025-11-04 16:25:53
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: events.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\events.py
# ================================================================================

from dataclasses import dataclass

@dataclass
class Evento:
    tipo: str
    payload: dict

PEDIDO_CREADO = "PedidoCreado"
PAGO_APROBADO = "PagoAprobado"
PEDIDO_LISTO = "PedidoListo"
DELIVERY_ASIGNADO = "DeliveryAsignado"
PEDIDO_ENTREGADO = "PedidoEntregado"
PEDIDO_CANCELADO = "PedidoCancelado"

# eventos “tiempo real”
PREPARACION_INICIADA = "PreparacionIniciada"
PREPARACION_AVANCE = "PreparacionAvance"   # payload: {pct, step}
SALIO_A_REPARTO = "SalioAReparto"
ESTADO = "Estado"

# NUEVO: confirmación de escritura del registro de compra
COMPRA_REGISTRADA = "CompraRegistrada"

# ================================================================================
# ARCHIVO 3/5: listeners.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\listeners.py
# ================================================================================

from datetime import datetime
import os
import json
import threading
import time

from core.events import COMPRA_REGISTRADA, PEDIDO_CREADO, PAGO_APROBADO, PEDIDO_LISTO, DELIVERY_ASIGNADO, PEDIDO_ENTREGADO, PEDIDO_CANCELADO, PREPARACION_INICIADA, PREPARACION_AVANCE, SALIO_A_REPARTO, ESTADO
from core.observers import Observer
from core.order_manager import OrderManager
from factories.notificacion_factory import NotificacionFactory
from persistencia.compra_repository import CompraRepository

# archivo JSONL de auditoría
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "data", "events.dat")

def _append_event_jsonl(evento):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            rec = {
                "ts": datetime.utcnow().isoformat() + "Z",
                "tipo": evento.tipo,
                "payload": evento.payload,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[AUDIT][ERROR] {e}")

class LogListener(Observer):
    def update(self, evento):
        print(f"[LOG] {evento.tipo} -> {evento.payload}")

class FileAuditListener(Observer):
    def update(self, evento):
        _append_event_jsonl(evento)

class ConsoleDashboard(Observer):
    ICONS = {
        PEDIDO_CREADO: "🛒",
        PAGO_APROBADO: "💳✅",
        PREPARACION_INICIADA: "👨‍🍳",
        PREPARACION_AVANCE: "⏳",
        PEDIDO_LISTO: "✅🍽️",
        DELIVERY_ASIGNADO: "🛵",
        SALIO_A_REPARTO: "➡️🛵",
        PEDIDO_ENTREGADO: "🎉📦",
        PEDIDO_CANCELADO: "❌",
        ESTADO: "ℹ️",
    }
    def update(self, evento):
        icon = self.ICONS.get(evento.tipo, "•")
        if evento.tipo == PREPARACION_AVANCE:
            pct = evento.payload.get("pct", 0)
            bars = int(pct // 10)
            bar = "█"*bars + "░"*(10-bars)
            print(f"[DASH] {icon} Prep {pct:>3}% [{bar}] (step={evento.payload.get('step')})")
        else:
            print(f"[DASH] {icon} {evento.tipo} :: {evento.payload}")

class CocinaRealtimeListener(Observer):
    """Simula preparación en background cuando llega PAGO_APROBADO."""
    def __init__(self, steps:int=8, step_time:float=0.2):
        self.steps = steps
        self.step_time = step_time
    def update(self, evento):
        if evento.tipo == PAGO_APROBADO:
            pedido_id = evento.payload.get("pedido_id")
            threading.Thread(target=self._prepare_async, args=(pedido_id,), daemon=True).start()
    def _prepare_async(self, pedido_id: str):
        om = OrderManager()
        om.publicar(type("Evt", (), {"tipo": PREPARACION_INICIADA, "payload": {"pedido_id": pedido_id}}))
        for i in range(1, self.steps+1):
            time.sleep(self.step_time)
            pct = int(i * 100 / self.steps)
            om.publicar(type("Evt", (), {"tipo": PREPARACION_AVANCE, "payload": {"pedido_id": pedido_id, "pct": pct, "step": i}}))
        om.publicar(type("Evt", (), {"tipo": PEDIDO_LISTO, "payload": {"pedido_id": pedido_id}}))

class CompraPersistListener(Observer):
    def update(self, evento):
        if evento.tipo == PEDIDO_ENTREGADO:
            # Esperamos un payload enriquecido con snapshot del pedido
            snap = evento.payload or {}
            # Guardamos registro
            CompraRepository.guardar(snap)
            # Avisamos que quedó registrado
            OrderManager().publicar(
                type("Evt", (), {"tipo": COMPRA_REGISTRADA, "payload": {"pedido_id": snap.get("pedido_id")}})
            )

# ================================================================================
# ARCHIVO 4/5: observers.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\observers.py
# ================================================================================

from abc import ABC, abstractmethod
class Observer(ABC):
    @abstractmethod
    def update(self, evento): 
        ...


# ================================================================================
# ARCHIVO 5/5: order_manager.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\order_manager.py
# ================================================================================

from typing import List

from core.events import Evento
from core.observers import Observer

class OrderManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._observers: List[Observer] = []
            cls._instance._log: list[str] = []
        return cls._instance

    def registrar(self, o: Observer):
        if o not in self._observers:
            self._observers.append(o)

    def publicar(self, evento: Evento):
        self._log.append(f"[EVENT] {evento.tipo} -> {evento.payload}")
        for o in list(self._observers):
            o.update(evento)

    def log(self) -> list[str]:
        return list(self._log)

