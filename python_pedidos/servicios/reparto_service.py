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