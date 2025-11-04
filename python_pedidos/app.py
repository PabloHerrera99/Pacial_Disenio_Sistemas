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