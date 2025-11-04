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
