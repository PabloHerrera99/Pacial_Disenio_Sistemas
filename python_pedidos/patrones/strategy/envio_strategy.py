from abc import ABC, abstractmethod
from constantes import COSTO_ENVIO_BASE_ARS, FACTOR_ENVIO
class EnvioStrategy(ABC):
    @abstractmethod
    def calcular_costo(self, pedido) -> float: ...
    @abstractmethod
    def estimar_tiempo(self, pedido) -> int: ...

class EnvioRapido(EnvioStrategy):
    def calcular_costo(self, pedido): return COSTO_ENVIO_BASE_ARS * FACTOR_ENVIO["rapido"]
    def estimar_tiempo(self, pedido): return 15
class EnvioEconomico(EnvioStrategy):
    def calcular_costo(self, pedido): return COSTO_ENVIO_BASE_ARS * FACTOR_ENVIO["economico"]
    def estimar_tiempo(self, pedido): return 30
class EnvioEcologico(EnvioStrategy):
    def calcular_costo(self, pedido): return COSTO_ENVIO_BASE_ARS * FACTOR_ENVIO["ecologico"]
    def estimar_tiempo(self, pedido): return 25
