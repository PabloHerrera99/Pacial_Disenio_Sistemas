"""
Archivo integrador generado automaticamente
Directorio: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\entidades
Fecha: 2025-11-04 16:25:53
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\entidades\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: menu.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\entidades\menu.py
# ================================================================================

from dataclasses import dataclass
@dataclass
class ItemMenu:
    nombre: str
    precio: float
    cantidad: int = 1
    def subtotal(self) -> float:
        return self.precio * self.cantidad


# ================================================================================
# ARCHIVO 3/4: pago.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\entidades\pago.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/4: pedido.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\entidades\pedido.py
# ================================================================================

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional
from entidades.menu import ItemMenu

class EstadoPedido(Enum):
    CREADO = auto(); PAGADO = auto(); EN_PREPARACION = auto(); LISTO = auto(); EN_CAMINO = auto(); ENTREGADO = auto(); CANCELADO = auto()
@dataclass
class Pedido:
    id: str
    items: List[ItemMenu]
    direccion: Optional[str] = None
    zona: str = "centro"
    total: float = field(default=0.0)


