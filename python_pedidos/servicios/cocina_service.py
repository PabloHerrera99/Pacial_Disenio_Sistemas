from core.order_manager import OrderManager
from core.events import Evento, PEDIDO_LISTO
class CocinaService:
    def iniciar_preparacion(self, pedido):
        OrderManager().publicar(Evento(PEDIDO_LISTO, {"pedido_id": pedido.id}))
