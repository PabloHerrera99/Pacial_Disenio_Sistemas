"""
Archivo integrador generado automaticamente
Directorio: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\persistencia
Fecha: 2025-11-04 16:25:53
Total de archivos integrados: 1
"""

# ================================================================================
# ARCHIVO 1/1: compra_repository.py
# Ruta: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\persistencia\compra_repository.py
# ================================================================================

import os, json
from datetime import datetime
from typing import List, Dict, Optional

# ruta: <raiz_proyecto>/data/compras.dat
DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data",
    "compras.dat"
)

class CompraRepository:
    @staticmethod
    def _ensure_file():
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        if not os.path.exists(DATA_FILE):
            open(DATA_FILE, "a", encoding="utf-8").close()

    @staticmethod
    def guardar(registro: Dict) -> None:
        """Guarda un registro de compra como JSONL."""
        CompraRepository._ensure_file()
        registro = dict(registro)
        registro.setdefault("ts", datetime.utcnow().isoformat() + "Z")
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")

    @staticmethod
    def listar() -> List[Dict]:
        """Devuelve todos los registros almacenados."""
        if not os.path.exists(DATA_FILE):
            return []
        out: List[Dict] = []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    # línea corrupta -> la ignoramos
                    pass
        return out

    @staticmethod
    def buscar_por_id(pedido_id: str) -> Optional[Dict]:
        """Retorna el primer registro que coincida con el pedido_id (o None)."""
        for r in CompraRepository.listar():
            if r.get("pedido_id") == pedido_id:
                return r
        return None


