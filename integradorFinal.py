"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas
Fecha de generacion: 2025-11-04 16:25:53
Total de archivos integrados: 37
Total de directorios procesados: 14
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. buscar_paquete.py
#
# DIRECTORIO: python_pedidos
#   2. __init__.py
#   3. app.py
#   4. constantes.py
#   5. main.py
#
# DIRECTORIO: python_pedidos\core
#   6. __init__.py
#   7. events.py
#   8. listeners.py
#   9. observers.py
#   10. order_manager.py
#
# DIRECTORIO: python_pedidos\entidades
#   11. __init__.py
#   12. menu.py
#   13. pago.py
#   14. pedido.py
#
# DIRECTORIO: python_pedidos\excepciones
#   15. __init__.py
#   16. pedidos_exception.py
#
# DIRECTORIO: python_pedidos\factories
#   17. __init__.py
#   18. notificacion_factory.py
#   19. pago_factory.py
#   20. pedido_factory.py
#
# DIRECTORIO: python_pedidos\patrones
#   21. __init__.py
#
# DIRECTORIO: python_pedidos\patrones\factory
#   22. __init__.py
#
# DIRECTORIO: python_pedidos\patrones\observer
#   23. __init__.py
#   24. observable.py
#   25. observer.py
#
# DIRECTORIO: python_pedidos\patrones\observer\eventos
#   26. __init__.py
#   27. evento_pedido.py
#
# DIRECTORIO: python_pedidos\patrones\singleton
#   28. __init__.py
#
# DIRECTORIO: python_pedidos\patrones\strategy
#   29. __init__.py
#   30. asignacion_strategy.py
#   31. envio_strategy.py
#
# DIRECTORIO: python_pedidos\persistencia
#   32. compra_repository.py
#
# DIRECTORIO: python_pedidos\servicios
#   33. __init__.py
#   34. cocina_service.py
#   35. pago_service.py
#   36. pedido_service.py
#   37. reparto_service.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/37: buscar_paquete.py
# Directorio: .
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\buscar_paquete.py
# ==============================================================================

"""
Script para buscar el paquete python_forestacion desde el directorio raiz del proyecto.
Incluye funcionalidad para integrar archivos Python en cada nivel del arbol de directorios.
"""
import os
import sys
from datetime import datetime


def buscar_paquete(directorio_raiz: str, nombre_paquete: str) -> list:
    """
    Busca un paquete Python en el directorio raiz y subdirectorios.

    Args:
        directorio_raiz: Directorio desde donde iniciar la busqueda
        nombre_paquete: Nombre del paquete a buscar

    Returns:
        Lista de rutas donde se encontro el paquete
    """
    paquetes_encontrados = []

    for raiz, directorios, archivos in os.walk(directorio_raiz):
        # Verificar si el directorio actual es el paquete buscado
        nombre_dir = os.path.basename(raiz)

        if nombre_dir == nombre_paquete:
            # Verificar que sea un paquete Python (contiene __init__.py)
            if '__init__.py' in archivos:
                paquetes_encontrados.append(raiz)
                print(f"[+] Paquete encontrado: {raiz}")
            else:
                print(f"[!] Directorio encontrado pero no es un paquete Python: {raiz}")

    return paquetes_encontrados


def obtener_archivos_python(directorio: str) -> list:
    """
    Obtiene todos los archivos Python en un directorio (sin recursion).

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de archivos .py
    """
    archivos_python = []
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isfile(ruta_completa) and item.endswith('.py'):
                # Excluir archivos integradores para evitar recursion infinita
                if item not in ['integrador.py', 'integradorFinal.py']:
                    archivos_python.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(archivos_python)


def obtener_subdirectorios(directorio: str) -> list:
    """
    Obtiene todos los subdirectorios inmediatos de un directorio.

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de subdirectorios
    """
    subdirectorios = []
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isdir(ruta_completa):
                # Excluir directorios especiales
                if not item.startswith('.') and item not in ['__pycache__', 'venv', '.venv']:
                    subdirectorios.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(subdirectorios)


def leer_contenido_archivo(ruta_archivo: str) -> str:
    """
    Lee el contenido de un archivo Python.

    Args:
        ruta_archivo: Ruta completa del archivo

    Returns:
        Contenido del archivo como string
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as error:
        print(f"[!] Error al leer {ruta_archivo}: {error}")
        return f"# Error al leer este archivo: {error}\n"


def crear_archivo_integrador(directorio: str, archivos_python: list) -> bool:
    """
    Crea un archivo integrador.py con el contenido de todos los archivos Python.

    Args:
        directorio: Directorio donde crear el archivo integrador
        archivos_python: Lista de rutas de archivos Python a integrar

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_python:
        return False

    ruta_integrador = os.path.join(directorio, 'integrador.py')

    try:
        with open(ruta_integrador, 'w', encoding='utf-8') as integrador:
            # Encabezado
            integrador.write('"""\n')
            integrador.write(f"Archivo integrador generado automaticamente\n")
            integrador.write(f"Directorio: {directorio}\n")
            integrador.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador.write(f"Total de archivos integrados: {len(archivos_python)}\n")
            integrador.write('"""\n\n')

            # Integrar cada archivo
            for idx, archivo in enumerate(archivos_python, 1):
                nombre_archivo = os.path.basename(archivo)
                integrador.write(f"# {'=' * 80}\n")
                integrador.write(f"# ARCHIVO {idx}/{len(archivos_python)}: {nombre_archivo}\n")
                integrador.write(f"# Ruta: {archivo}\n")
                integrador.write(f"# {'=' * 80}\n\n")

                contenido = leer_contenido_archivo(archivo)
                integrador.write(contenido)
                integrador.write("\n\n")

        print(f"[OK] Integrador creado: {ruta_integrador}")
        print(f"     Archivos integrados: {len(archivos_python)}")
        return True

    except Exception as error:
        print(f"[!] Error al crear integrador en {directorio}: {error}")
        return False


def procesar_directorio_recursivo(directorio: str, nivel: int = 0, archivos_totales: list = None) -> list:
    """
    Procesa un directorio de forma recursiva, creando integradores en cada nivel.
    Utiliza DFS (Depth-First Search) para llegar primero a los niveles mas profundos.

    Args:
        directorio: Directorio a procesar
        nivel: Nivel de profundidad actual (para logging)
        archivos_totales: Lista acumulativa de todos los archivos procesados

    Returns:
        Lista de todos los archivos Python procesados en el arbol
    """
    if archivos_totales is None:
        archivos_totales = []

    indentacion = "  " * nivel
    print(f"{indentacion}[INFO] Procesando nivel {nivel}: {os.path.basename(directorio)}")

    # Obtener subdirectorios
    subdirectorios = obtener_subdirectorios(directorio)

    # Primero, procesar recursivamente todos los subdirectorios (DFS)
    for subdir in subdirectorios:
        procesar_directorio_recursivo(subdir, nivel + 1, archivos_totales)

    # Despues de procesar subdirectorios, procesar archivos del nivel actual
    archivos_python = obtener_archivos_python(directorio)

    if archivos_python:
        print(f"{indentacion}[+] Encontrados {len(archivos_python)} archivo(s) Python")
        crear_archivo_integrador(directorio, archivos_python)
        # Agregar archivos a la lista total
        archivos_totales.extend(archivos_python)
    else:
        print(f"{indentacion}[INFO] No hay archivos Python en este nivel")

    return archivos_totales


def crear_integrador_final(directorio_raiz: str, archivos_totales: list) -> bool:
    """
    Crea un archivo integradorFinal.py con TODO el codigo fuente de todas las ramas.

    Args:
        directorio_raiz: Directorio donde crear el archivo integrador final
        archivos_totales: Lista completa de todos los archivos Python procesados

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_totales:
        print("[!] No hay archivos para crear el integrador final")
        return False

    ruta_integrador_final = os.path.join(directorio_raiz, 'integradorFinal.py')

    # Organizar archivos por directorio para mejor estructura
    archivos_por_directorio = {}
    for archivo in archivos_totales:
        directorio = os.path.dirname(archivo)
        if directorio not in archivos_por_directorio:
            archivos_por_directorio[directorio] = []
        archivos_por_directorio[directorio].append(archivo)

    try:
        with open(ruta_integrador_final, 'w', encoding='utf-8') as integrador_final:
            # Encabezado principal
            integrador_final.write('"""\n')
            integrador_final.write("INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write(f"Directorio raiz: {directorio_raiz}\n")
            integrador_final.write(f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write(f"Total de archivos integrados: {len(archivos_totales)}\n")
            integrador_final.write(f"Total de directorios procesados: {len(archivos_por_directorio)}\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write('"""\n\n')

            # Tabla de contenidos
            integrador_final.write("# " + "=" * 78 + "\n")
            integrador_final.write("# TABLA DE CONTENIDOS\n")
            integrador_final.write("# " + "=" * 78 + "\n\n")

            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)
                    integrador_final.write(f"#   {contador_global}. {nombre_archivo}\n")
                    contador_global += 1
                integrador_final.write("#\n")

            integrador_final.write("\n\n")

            # Contenido completo organizado por directorio
            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)

                # Separador de directorio
                integrador_final.write("\n" + "#" * 80 + "\n")
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                integrador_final.write("#" * 80 + "\n\n")

                # Procesar cada archivo del directorio
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)

                    integrador_final.write(f"# {'=' * 78}\n")
                    integrador_final.write(f"# ARCHIVO {contador_global}/{len(archivos_totales)}: {nombre_archivo}\n")
                    integrador_final.write(f"# Directorio: {dir_relativo}\n")
                    integrador_final.write(f"# Ruta completa: {archivo}\n")
                    integrador_final.write(f"# {'=' * 78}\n\n")

                    contenido = leer_contenido_archivo(archivo)
                    integrador_final.write(contenido)
                    integrador_final.write("\n\n")

                    contador_global += 1

            # Footer
            integrador_final.write("\n" + "#" * 80 + "\n")
            integrador_final.write("# FIN DEL INTEGRADOR FINAL\n")
            integrador_final.write(f"# Total de archivos: {len(archivos_totales)}\n")
            integrador_final.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write("#" * 80 + "\n")

        print(f"\n[OK] Integrador final creado: {ruta_integrador_final}")
        print(f"     Total de archivos integrados: {len(archivos_totales)}")
        print(f"     Total de directorios procesados: {len(archivos_por_directorio)}")

        # Mostrar tamanio del archivo
        tamanio = os.path.getsize(ruta_integrador_final)
        if tamanio < 1024:
            tamanio_str = f"{tamanio} bytes"
        elif tamanio < 1024 * 1024:
            tamanio_str = f"{tamanio / 1024:.2f} KB"
        else:
            tamanio_str = f"{tamanio / (1024 * 1024):.2f} MB"
        print(f"     Tamanio del archivo: {tamanio_str}")

        return True

    except Exception as error:
        print(f"[!] Error al crear integrador final: {error}")
        return False


def integrar_arbol_directorios(directorio_raiz: str) -> None:
    """
    Inicia el proceso de integracion para todo el arbol de directorios.

    Args:
        directorio_raiz: Directorio raiz desde donde comenzar
    """
    print("\n" + "=" * 80)
    print("INICIANDO INTEGRACION DE ARCHIVOS PYTHON")
    print("=" * 80)
    print(f"Directorio raiz: {directorio_raiz}\n")

    # Procesar directorios y obtener lista de todos los archivos
    archivos_totales = procesar_directorio_recursivo(directorio_raiz)

    print("\n" + "=" * 80)
    print("INTEGRACION POR NIVELES COMPLETADA")
    print("=" * 80)

    # Crear integrador final con todos los archivos
    if archivos_totales:
        print("\n" + "=" * 80)
        print("CREANDO INTEGRADOR FINAL")
        print("=" * 80)
        crear_integrador_final(directorio_raiz, archivos_totales)

    print("\n" + "=" * 80)
    print("PROCESO COMPLETO FINALIZADO")
    print("=" * 80)


def main():
    """Funcion principal del script."""
    # Obtener el directorio raiz del proyecto (donde esta este script)
    directorio_raiz = os.path.dirname(os.path.abspath(__file__))

    # Verificar argumentos de linea de comandos
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()

        if comando == "integrar":
            # Modo de integracion de archivos
            if len(sys.argv) > 2:
                directorio_objetivo = sys.argv[2]
                if not os.path.isabs(directorio_objetivo):
                    directorio_objetivo = os.path.join(directorio_raiz, directorio_objetivo)
            else:
                directorio_objetivo = directorio_raiz

            if not os.path.isdir(directorio_objetivo):
                print(f"[!] El directorio no existe: {directorio_objetivo}")
                return 1

            integrar_arbol_directorios(directorio_objetivo)
            return 0

        elif comando == "help" or comando == "--help" or comando == "-h":
            print("Uso: python buscar_paquete.py [COMANDO] [OPCIONES]")
            print("")
            print("Comandos disponibles:")
            print("  (sin argumentos)     Busca el paquete python_forestacion")
            print("  integrar [DIR]       Integra archivos Python en el arbol de directorios")
            print("                       DIR: directorio raiz (por defecto: directorio actual)")
            print("  help                 Muestra esta ayuda")
            print("")
            print("Ejemplos:")
            print("  python buscar_paquete.py")
            print("  python buscar_paquete.py integrar")
            print("  python buscar_paquete.py integrar python_forestacion")
            return 0

        else:
            print(f"[!] Comando desconocido: {comando}")
            print("    Use 'python buscar_paquete.py help' para ver los comandos disponibles")
            return 1

    # Modo por defecto: buscar paquete
    print(f"[INFO] Buscando desde: {directorio_raiz}")
    print(f"[INFO] Buscando paquete: python_forestacion")
    print("")

    # Buscar el paquete
    paquetes = buscar_paquete(directorio_raiz, "python_pedidos")

    print("")
    if paquetes:
        print(f"[OK] Se encontraron {len(paquetes)} paquete(s):")
        for paquete in paquetes:
            print(f"  - {paquete}")

            # Mostrar estructura basica del paquete
            print(f"    Contenido:")
            try:
                contenido = os.listdir(paquete)
                for item in sorted(contenido)[:10]:  # Mostrar primeros 10 items
                    ruta_item = os.path.join(paquete, item)
                    if os.path.isdir(ruta_item):
                        print(f"      [DIR]  {item}")
                    else:
                        print(f"      [FILE] {item}")
                if len(contenido) > 10:
                    print(f"      ... y {len(contenido) - 10} items mas")
            except PermissionError:
                print(f"      [!] Sin permisos para leer el directorio")
    else:
        print("[!] No se encontro el paquete python_forestacion")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())


################################################################################
# DIRECTORIO: python_pedidos
################################################################################

# ==============================================================================
# ARCHIVO 2/37: __init__.py
# Directorio: python_pedidos
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 3/37: app.py
# Directorio: python_pedidos
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\app.py
# ==============================================================================

import time
from core.order_manager import OrderManager
from core.listeners import CocinaRealtimeListener, CompraPersistListener, ConsoleDashboard, FileAuditListener, LogListener
from persistencia.compra_repository import CompraRepository
from servicios.pedido_service import PedidoService
from patrones.strategy.asignacion_strategy import AsignacionCercano, Repartidor
from entidades.menu import ItemMenu
from servicios.reparto_service import RepartoService


def run_demo():
    om = OrderManager()
    # Observers: log + dashboard + persistencia + cocina en tiempo real + persistencia de compras
    om.registrar(LogListener())
    om.registrar(ConsoleDashboard())
    om.registrar(FileAuditListener())
    om.registrar(CocinaRealtimeListener(steps=8, step_time=0.2))
    om.registrar(CompraPersistListener())  # NUEVO

    # Pool de repartidores y servicios
    pool = [Repartidor("Mica", "centro"), Repartidor("Juan", "oeste"), Repartidor("Luz", "norte")]
    pedido_service = PedidoService(RepartoService(AsignacionCercano(pool)))

    # Crear pedido
    items = [ItemMenu("Hamburguesa", 3500, 1), ItemMenu("Papas", 1500, 1), ItemMenu("Bebida", 1200, 2)]
    pedido = pedido_service.crear_pedido("P-RT-001", items, tipo="delivery", envio="rapido",
                                         direccion="Av. Siempre Viva 742", zona="centro")

    # Pagar (dispara preparación en background por el observer)
    ok = pedido_service.pagar(pedido, tipo_pago="Tarjeta")
    if not ok:
        print("Pago rechazado, abortando"); return

    # Esperar algunos ticks de preparación antes de asignar delivery
    time.sleep(1.0)

    # Asignar delivery
    r = pedido_service.asignar_delivery(pedido)
    print(f"Repartidor asignado: {r.nombre} (carga={r.carga})")

    # Esperar a que finalice la preparación simulada
    time.sleep(2.0)

    # Entrega (dispara persistencia en compras.dat)
    pedido_service.marcar_entregado(pedido)

    # === Recuperación de compras guardadas ===
    print("\n=== COMPRAS REGISTRADAS (listar) ===")
    for compra in CompraRepository.listar():
        print(compra)

    print("\n=== BUSCAR POR ID 'P-RT-001' ===")
    print(CompraRepository.buscar_por_id("P-RT-001"))

    # === Log acumulado ===
    print("\n=== LOG ACUMULADO ===")
    for line in OrderManager().log():
        print(line)

# ==============================================================================
# ARCHIVO 4/37: constantes.py
# Directorio: python_pedidos
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\constantes.py
# ==============================================================================

TIEMPO_PREPARACION_BASE_MIN = 5
COSTO_ENVIO_BASE_ARS = 500.0
FACTOR_ENVIO = {"rapido": 1.5, "economico": 0.7, "ecologico": 0.9}


# ==============================================================================
# ARCHIVO 5/37: main.py
# Directorio: python_pedidos
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\main.py
# ==============================================================================

from app import run_demo

if __name__ == "__main__":
    run_demo()



################################################################################
# DIRECTORIO: python_pedidos\core
################################################################################

# ==============================================================================
# ARCHIVO 6/37: __init__.py
# Directorio: python_pedidos\core
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 7/37: events.py
# Directorio: python_pedidos\core
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\events.py
# ==============================================================================

from dataclasses import dataclass

@dataclass
class Evento:
    tipo: str
    payload: dict

PEDIDO_CREADO = "PedidoCreado"
PAGO_APROBADO = "PagoAprobado"
PEDIDO_LISTO = "PedidoListo"
DELIVERY_ASIGNADO = "DeliveryAsignado"
PEDIDO_ENTREGADO = "PedidoEntregado"
PEDIDO_CANCELADO = "PedidoCancelado"

# eventos “tiempo real”
PREPARACION_INICIADA = "PreparacionIniciada"
PREPARACION_AVANCE = "PreparacionAvance"   # payload: {pct, step}
SALIO_A_REPARTO = "SalioAReparto"
ESTADO = "Estado"

# NUEVO: confirmación de escritura del registro de compra
COMPRA_REGISTRADA = "CompraRegistrada"

# ==============================================================================
# ARCHIVO 8/37: listeners.py
# Directorio: python_pedidos\core
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\listeners.py
# ==============================================================================

from datetime import datetime
import os
import json
import threading
import time

from core.events import COMPRA_REGISTRADA, PEDIDO_CREADO, PAGO_APROBADO, PEDIDO_LISTO, DELIVERY_ASIGNADO, PEDIDO_ENTREGADO, PEDIDO_CANCELADO, PREPARACION_INICIADA, PREPARACION_AVANCE, SALIO_A_REPARTO, ESTADO
from core.observers import Observer
from core.order_manager import OrderManager
from factories.notificacion_factory import NotificacionFactory
from persistencia.compra_repository import CompraRepository

# archivo JSONL de auditoría
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "data", "events.dat")

def _append_event_jsonl(evento):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            rec = {
                "ts": datetime.utcnow().isoformat() + "Z",
                "tipo": evento.tipo,
                "payload": evento.payload,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[AUDIT][ERROR] {e}")

class LogListener(Observer):
    def update(self, evento):
        print(f"[LOG] {evento.tipo} -> {evento.payload}")

class FileAuditListener(Observer):
    def update(self, evento):
        _append_event_jsonl(evento)

class ConsoleDashboard(Observer):
    ICONS = {
        PEDIDO_CREADO: "🛒",
        PAGO_APROBADO: "💳✅",
        PREPARACION_INICIADA: "👨‍🍳",
        PREPARACION_AVANCE: "⏳",
        PEDIDO_LISTO: "✅🍽️",
        DELIVERY_ASIGNADO: "🛵",
        SALIO_A_REPARTO: "➡️🛵",
        PEDIDO_ENTREGADO: "🎉📦",
        PEDIDO_CANCELADO: "❌",
        ESTADO: "ℹ️",
    }
    def update(self, evento):
        icon = self.ICONS.get(evento.tipo, "•")
        if evento.tipo == PREPARACION_AVANCE:
            pct = evento.payload.get("pct", 0)
            bars = int(pct // 10)
            bar = "█"*bars + "░"*(10-bars)
            print(f"[DASH] {icon} Prep {pct:>3}% [{bar}] (step={evento.payload.get('step')})")
        else:
            print(f"[DASH] {icon} {evento.tipo} :: {evento.payload}")

class CocinaRealtimeListener(Observer):
    """Simula preparación en background cuando llega PAGO_APROBADO."""
    def __init__(self, steps:int=8, step_time:float=0.2):
        self.steps = steps
        self.step_time = step_time
    def update(self, evento):
        if evento.tipo == PAGO_APROBADO:
            pedido_id = evento.payload.get("pedido_id")
            threading.Thread(target=self._prepare_async, args=(pedido_id,), daemon=True).start()
    def _prepare_async(self, pedido_id: str):
        om = OrderManager()
        om.publicar(type("Evt", (), {"tipo": PREPARACION_INICIADA, "payload": {"pedido_id": pedido_id}}))
        for i in range(1, self.steps+1):
            time.sleep(self.step_time)
            pct = int(i * 100 / self.steps)
            om.publicar(type("Evt", (), {"tipo": PREPARACION_AVANCE, "payload": {"pedido_id": pedido_id, "pct": pct, "step": i}}))
        om.publicar(type("Evt", (), {"tipo": PEDIDO_LISTO, "payload": {"pedido_id": pedido_id}}))

class CompraPersistListener(Observer):
    def update(self, evento):
        if evento.tipo == PEDIDO_ENTREGADO:
            # Esperamos un payload enriquecido con snapshot del pedido
            snap = evento.payload or {}
            # Guardamos registro
            CompraRepository.guardar(snap)
            # Avisamos que quedó registrado
            OrderManager().publicar(
                type("Evt", (), {"tipo": COMPRA_REGISTRADA, "payload": {"pedido_id": snap.get("pedido_id")}})
            )

# ==============================================================================
# ARCHIVO 9/37: observers.py
# Directorio: python_pedidos\core
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\observers.py
# ==============================================================================

from abc import ABC, abstractmethod
class Observer(ABC):
    @abstractmethod
    def update(self, evento): 
        ...


# ==============================================================================
# ARCHIVO 10/37: order_manager.py
# Directorio: python_pedidos\core
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\core\order_manager.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: python_pedidos\entidades
################################################################################

# ==============================================================================
# ARCHIVO 11/37: __init__.py
# Directorio: python_pedidos\entidades
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\entidades\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 12/37: menu.py
# Directorio: python_pedidos\entidades
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\entidades\menu.py
# ==============================================================================

from dataclasses import dataclass
@dataclass
class ItemMenu:
    nombre: str
    precio: float
    cantidad: int = 1
    def subtotal(self) -> float:
        return self.precio * self.cantidad


# ==============================================================================
# ARCHIVO 13/37: pago.py
# Directorio: python_pedidos\entidades
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\entidades\pago.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 14/37: pedido.py
# Directorio: python_pedidos\entidades
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\entidades\pedido.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: python_pedidos\excepciones
################################################################################

# ==============================================================================
# ARCHIVO 15/37: __init__.py
# Directorio: python_pedidos\excepciones
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\excepciones\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 16/37: pedidos_exception.py
# Directorio: python_pedidos\excepciones
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\excepciones\pedidos_exception.py
# ==============================================================================

class PedidosException(Exception): pass



################################################################################
# DIRECTORIO: python_pedidos\factories
################################################################################

# ==============================================================================
# ARCHIVO 17/37: __init__.py
# Directorio: python_pedidos\factories
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\factories\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 18/37: notificacion_factory.py
# Directorio: python_pedidos\factories
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\factories\notificacion_factory.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 19/37: pago_factory.py
# Directorio: python_pedidos\factories
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\factories\pago_factory.py
# ==============================================================================

from entidades.pago import Pago
class PagoFactory:
    @staticmethod
    def crear(tipo: str) -> Pago:
        return Pago(metodo=tipo)


# ==============================================================================
# ARCHIVO 20/37: pedido_factory.py
# Directorio: python_pedidos\factories
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\factories\pedido_factory.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: python_pedidos\patrones
################################################################################

# ==============================================================================
# ARCHIVO 21/37: __init__.py
# Directorio: python_pedidos\patrones
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: python_pedidos\patrones\factory
################################################################################

# ==============================================================================
# ARCHIVO 22/37: __init__.py
# Directorio: python_pedidos\patrones\factory
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\factory\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: python_pedidos\patrones\observer
################################################################################

# ==============================================================================
# ARCHIVO 23/37: __init__.py
# Directorio: python_pedidos\patrones\observer
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\observer\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 24/37: observable.py
# Directorio: python_pedidos\patrones\observer
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\observer\observable.py
# ==============================================================================

class Observable: pass


# ==============================================================================
# ARCHIVO 25/37: observer.py
# Directorio: python_pedidos\patrones\observer
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\observer\observer.py
# ==============================================================================

class Observer: pass



################################################################################
# DIRECTORIO: python_pedidos\patrones\observer\eventos
################################################################################

# ==============================================================================
# ARCHIVO 26/37: __init__.py
# Directorio: python_pedidos\patrones\observer\eventos
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\observer\eventos\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 27/37: evento_pedido.py
# Directorio: python_pedidos\patrones\observer\eventos
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\observer\eventos\evento_pedido.py
# ==============================================================================

# opcional



################################################################################
# DIRECTORIO: python_pedidos\patrones\singleton
################################################################################

# ==============================================================================
# ARCHIVO 28/37: __init__.py
# Directorio: python_pedidos\patrones\singleton
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\singleton\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: python_pedidos\patrones\strategy
################################################################################

# ==============================================================================
# ARCHIVO 29/37: __init__.py
# Directorio: python_pedidos\patrones\strategy
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\strategy\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 30/37: asignacion_strategy.py
# Directorio: python_pedidos\patrones\strategy
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\strategy\asignacion_strategy.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 31/37: envio_strategy.py
# Directorio: python_pedidos\patrones\strategy
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\patrones\strategy\envio_strategy.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: python_pedidos\persistencia
################################################################################

# ==============================================================================
# ARCHIVO 32/37: compra_repository.py
# Directorio: python_pedidos\persistencia
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\persistencia\compra_repository.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: python_pedidos\servicios
################################################################################

# ==============================================================================
# ARCHIVO 33/37: __init__.py
# Directorio: python_pedidos\servicios
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 34/37: cocina_service.py
# Directorio: python_pedidos\servicios
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\cocina_service.py
# ==============================================================================

from core.order_manager import OrderManager
from core.events import Evento, PEDIDO_LISTO
class CocinaService:
    def iniciar_preparacion(self, pedido):
        OrderManager().publicar(Evento(PEDIDO_LISTO, {"pedido_id": pedido.id}))


# ==============================================================================
# ARCHIVO 35/37: pago_service.py
# Directorio: python_pedidos\servicios
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\pago_service.py
# ==============================================================================

from factories.pago_factory import PagoFactory
from core.order_manager import OrderManager
from core.events import Evento, PAGO_APROBADO, PEDIDO_CANCELADO
class PagoService:
    def pagar(self, pedido, tipo_pago: str) -> bool:
        pago = PagoFactory.crear(tipo_pago)
        ok = pago.autorizar(pedido.total)
        om = OrderManager()
        if ok:
            om.publicar(Evento(PAGO_APROBADO, {"pedido_id": pedido.id, "monto": pedido.total, "metodo": tipo_pago}))
            return True
        else:
            om.publicar(Evento(PEDIDO_CANCELADO, {"pedido_id": pedido.id, "motivo": "Pago rechazado"}))
            return False


# ==============================================================================
# ARCHIVO 36/37: pedido_service.py
# Directorio: python_pedidos\servicios
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\pedido_service.py
# ==============================================================================


from core.order_manager import OrderManager
from servicios.reparto_service import RepartoService
from servicios.pago_service import PagoService
from servicios.cocina_service import CocinaService
from core.events import PEDIDO_CREADO, PEDIDO_ENTREGADO
from core.events import Evento
from factories.pedido_factory import PedidoFactory


class PedidoService:
    def __init__(self, reparto_service: RepartoService):
        self._reparto = reparto_service
        self._pago = PagoService()
        self._cocina = CocinaService()

    def crear_pedido(self, pedido_id: str, items, tipo: str, **kwargs):
        p = PedidoFactory.crear(pedido_id, items, tipo, **kwargs)
        OrderManager().publicar(Evento(PEDIDO_CREADO, {"pedido_id": p.id, "total": p.total}))
        return p

    def pagar(self, pedido, tipo_pago: str) -> bool:
        return self._pago.pagar(pedido, tipo_pago)

    def preparar(self, pedido):
        self._cocina.iniciar_preparacion(pedido)

    def asignar_delivery(self, pedido):
        return self._reparto.asignar(pedido)

    def marcar_entregado(self, pedido):
        # Snapshot mínimo para persistir la compra
        snap = {
            "pedido_id": pedido.id,
            "items": [{"nombre": it.nombre, "precio": it.precio, "cantidad": it.cantidad} for it in pedido.items],
            "total": pedido.total,
            "direccion": getattr(pedido, "direccion", None),
            "zona": getattr(pedido, "zona", None),
            "estado_final": "ENTREGADO",
        }
        OrderManager().publicar(Evento(PEDIDO_ENTREGADO, snap))


# ==============================================================================
# ARCHIVO 37/37: reparto_service.py
# Directorio: python_pedidos\servicios
# Ruta completa: C:\Users\pablo\OneDrive\Documentos\Facultad\Diseño de Sistemas\PythonPedidos\Pacial_Disenio_Sistemas\python_pedidos\servicios\reparto_service.py
# ==============================================================================

from core.order_manager import OrderManager
from core.events import SALIO_A_REPARTO, Evento, DELIVERY_ASIGNADO
from patrones.strategy.asignacion_strategy import AsignacionStrategy, Repartidor

class RepartoService:
    def __init__(self, strategy: AsignacionStrategy):
        self._strategy = strategy
    def set_strategy(self, s: AsignacionStrategy):
        self._strategy = s
    def asignar(self, pedido):
        r: Repartidor = self._strategy.asignar_repartidor(pedido)
        om = OrderManager()
        om.publicar(Evento(DELIVERY_ASIGNADO, {"pedido_id": pedido.id, "repartidor": r.nombre}))
        om.publicar(Evento(SALIO_A_REPARTO, {"pedido_id": pedido.id, "repartidor": r.nombre}))
        return r


################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 37
# Generado: 2025-11-04 16:25:53
################################################################################
