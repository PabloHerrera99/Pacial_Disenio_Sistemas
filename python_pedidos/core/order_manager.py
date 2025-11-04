from typing import List

from core.events import Evento
from core.observers import Observer

class OrderManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._observers: List[Observer] = []
            cls._instance._log: list[str] = []
        return cls._instance

    def registrar(self, o: Observer):
        if o not in self._observers:
            self._observers.append(o)

    def publicar(self, evento: Evento):
        self._log.append(f"[EVENT] {evento.tipo} -> {evento.payload}")
        for o in list(self._observers):
            o.update(evento)

    def log(self) -> list[str]:
        return list(self._log)