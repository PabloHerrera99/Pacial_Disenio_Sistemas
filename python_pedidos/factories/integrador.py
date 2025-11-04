"""
Archivo integrador generado automaticamente
Directorio: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\factories
Fecha: 2025-11-04 16:25:53
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\factories\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: notificacion_factory.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\factories\notificacion_factory.py
# ================================================================================

from abc import ABC, abstractmethod
class Notificador(ABC):
    @abstractmethod
    def enviar(self, msg: str, destino: str) -> None: ...
class EmailNotificador(Notificador):
    def enviar(self, msg: str, destino: str) -> None: print(f"[EMAIL] a {destino}: {msg}")
class SMSNotificador(Notificador):
    def enviar(self, msg: str, destino: str) -> None: print(f"[SMS] a {destino}: {msg}")
class PushNotificador(Notificador):
    def enviar(self, msg: str, destino: str) -> None: print(f"[PUSH] a {destino}: {msg}")
class NotificacionFactory:
    @staticmethod
    def crear(tipo: str) -> Notificador:
        t = tipo.lower()
        if t == "email": return EmailNotificador()
        if t == "sms": return SMSNotificador()
        return PushNotificador()


# ================================================================================
# ARCHIVO 3/4: pago_factory.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\factories\pago_factory.py
# ================================================================================

from entidades.pago import Pago
class PagoFactory:
    @staticmethod
    def crear(tipo: str) -> Pago:
        return Pago(metodo=tipo)


# ================================================================================
# ARCHIVO 4/4: pedido_factory.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\factories\pedido_factory.py
# ================================================================================

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


