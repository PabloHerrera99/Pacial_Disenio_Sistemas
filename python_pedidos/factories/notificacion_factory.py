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
