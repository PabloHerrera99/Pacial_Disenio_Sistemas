from dataclasses import dataclass
@dataclass
class ItemMenu:
    nombre: str
    precio: float
    cantidad: int = 1
    def subtotal(self) -> float:
        return self.precio * self.cantidad
