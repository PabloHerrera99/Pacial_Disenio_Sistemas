from abc import ABC, abstractmethod
from dataclasses import dataclass
@dataclass
class Repartidor:
    nombre: str; zona: str; carga: int = 0
class AsignacionStrategy(ABC):

    @abstractmethod
    def asignar_repartidor(self, pedido) -> Repartidor: ...

class AsignacionCercano(AsignacionStrategy):
    def __init__(self, pool): self.pool = pool
    def asignar_repartidor(self, pedido) -> Repartidor:
        for r in self.pool:
            if r.zona == getattr(pedido, "zona", "centro"):
                r.carga += 1; return r
        self.pool[0].carga += 1; return self.pool[0]
    
class AsignacionBalanceada(AsignacionStrategy):
    def __init__(self, pool): self.pool = pool
    def asignar_repartidor(self, pedido) -> Repartidor:
        r = min(self.pool, key=lambda x: x.carga); r.carga += 1; return r
