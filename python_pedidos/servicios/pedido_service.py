
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
