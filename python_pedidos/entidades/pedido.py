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
