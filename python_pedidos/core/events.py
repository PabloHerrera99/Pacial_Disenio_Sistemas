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