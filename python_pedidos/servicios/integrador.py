"""
Archivo integrador generado automaticamente
Directorio: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios
Fecha: 2025-11-04 16:25:53
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: cocina_service.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\cocina_service.py
# ================================================================================

from core.order_manager import OrderManager
from core.events import Evento, PEDIDO_LISTO
class CocinaService:
    def iniciar_preparacion(self, pedido):
        OrderManager().publicar(Evento(PEDIDO_LISTO, {"pedido_id": pedido.id}))


# ================================================================================
# ARCHIVO 3/5: pago_service.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\pago_service.py
# ================================================================================

from factories.pago_factory import PagoFactory
from core.order_manager import OrderManager
from core.events import Evento, PAGO_APROBADO, PEDIDO_CANCELADO
class PagoService:
    def pagar(self, pedido, tipo_pago: str) -> bool:
        pago = PagoFactory.crear(tipo_pago)
        ok = pago.autorizar(pedido.total)
        om = OrderManager()
        if ok:
            om.publicar(Evento(PAGO_APROBADO, {"pedido_id": pedido.id, "monto": pedido.total, "metodo": tipo_pago}))
            return True
        else:
            om.publicar(Evento(PEDIDO_CANCELADO, {"pedido_id": pedido.id, "motivo": "Pago rechazado"}))
            return False


# ================================================================================
# ARCHIVO 4/5: pedido_service.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\pedido_service.py
# ================================================================================


from core.order_manager import OrderManager
from servicios.reparto_service import RepartoService
from servicios.pago_service import PagoService
from servicios.cocina_service import CocinaService
from core.events import PEDIDO_CREADO, PEDIDO_ENTREGADO
from core.events import Evento
from factories.pedido_factory import PedidoFactory


class PedidoService:
    def __init__(self, reparto_service: RepartoService):
        self._reparto = reparto_service
        self._pago = PagoService()
        self._cocina = CocinaService()

    def crear_pedido(self, pedido_id: str, items, tipo: str, **kwargs):
        p = PedidoFactory.crear(pedido_id, items, tipo, **kwargs)
        OrderManager().publicar(Evento(PEDIDO_CREADO, {"pedido_id": p.id, "total": p.total}))
        return p

    def pagar(self, pedido, tipo_pago: str) -> bool:
        return self._pago.pagar(pedido, tipo_pago)

    def preparar(self, pedido):
        self._cocina.iniciar_preparacion(pedido)

    def asignar_delivery(self, pedido):
        return self._reparto.asignar(pedido)

    def marcar_entregado(self, pedido):
        # Snapshot mínimo para persistir la compra
        snap = {
            "pedido_id": pedido.id,
            "items": [{"nombre": it.nombre, "precio": it.precio, "cantidad": it.cantidad} for it in pedido.items],
            "total": pedido.total,
            "direccion": getattr(pedido, "direccion", None),
            "zona": getattr(pedido, "zona", None),
            "estado_final": "ENTREGADO",
        }
        OrderManager().publicar(Evento(PEDIDO_ENTREGADO, snap))


# ================================================================================
# ARCHIVO 5/5: reparto_service.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\reparto_service.py
# ================================================================================

from core.order_manager import OrderManager
from core.events import SALIO_A_REPARTO, Evento, DELIVERY_ASIGNADO
from patrones.strategy.asignacion_strategy import AsignacionStrategy, Repartidor

class RepartoService:
    def __init__(self, strategy: AsignacionStrategy):
        self._strategy = strategy
    def set_strategy(self, s: AsignacionStrategy):
        self._strategy = s
    def asignar(self, pedido):
        r: Repartidor = self._strategy.asignar_repartidor(pedido)
        om = OrderManager()
        om.publicar(Evento(DELIVERY_ASIGNADO, {"pedido_id": pedido.id, "repartidor": r.nombre}))
        om.publicar(Evento(SALIO_A_REPARTO, {"pedido_id": pedido.id, "repartidor": r.nombre}))
        return r

