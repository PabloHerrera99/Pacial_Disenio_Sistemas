from entidades.pedido import Pedido
from patrones.strategy.envio_strategy import EnvioRapido, EnvioEconomico, EnvioEcologico
class PedidoFactory:
    @staticmethod
    def crear(pedido_id: str, items, tipo: str, **kwargs) -> Pedido:
        envio = kwargs.get("envio")
        if isinstance(envio, str):
            envios = {"rapido": EnvioRapido, "economico": EnvioEconomico, "ecologico": EnvioEcologico}
            envio = envios.get(envio.lower(), lambda: None)()
        p = Pedido(id=pedido_id, items=items, direccion=kwargs.get("direccion"), zona=kwargs.get("zona","centro"))
        items_total = sum(i.subtotal() for i in items)
        envio_costo = envio.calcular_costo(p) if envio else 0.0
        p.total = round(items_total + envio_costo, 2)
        return p
