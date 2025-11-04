from enum import Enum, auto
class EstadoPago(Enum):
    INICIADO = auto(); APROBADO = auto(); RECHAZADO = auto()
class Pago:
    def __init__(self, metodo: str):
        self.metodo = metodo
        self.estado = EstadoPago.INICIADO
    def autorizar(self, monto: float) -> bool:
        if monto <= 0 or self.metodo.lower() == "rechazo":
            self.estado = EstadoPago.RECHAZADO; return False
        self.estado = EstadoPago.APROBADO; return True
