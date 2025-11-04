"""
Archivo integrador generado automaticamente
Directorio: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\strategy
Fecha: 2025-11-04 16:25:53
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\strategy\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: asignacion_strategy.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\strategy\asignacion_strategy.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/3: envio_strategy.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\strategy\envio_strategy.py
# ================================================================================

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


