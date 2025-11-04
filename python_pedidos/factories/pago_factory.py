from entidades.pago import Pago
class PagoFactory:
    @staticmethod
    def crear(tipo: str) -> Pago:
        return Pago(metodo=tipo)
