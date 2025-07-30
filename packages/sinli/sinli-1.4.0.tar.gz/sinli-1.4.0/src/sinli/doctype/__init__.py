from enum import Enum
from . import libros
from . import pedido
from . import envio
from . import factul
from . import mensaj
from . import devolu
from . import abono
from . import liqve2

class DocumentType(Enum):
    ABONO = ("Albarán o Factura de Abono",  {
        "02": abono.v2.AbonoDoc
    })
    CAMPRE = ("Cambios de precio", None)
    DEVOLU = ("Devoluciones", {
        "02": devolu.v2.DevolucionDoc,
        "03": devolu.v3.DevolucionDoc,
        "??": devolu.v3.DevolucionDoc,
    })
    ENVIO = ("Albarán de envío de distribuidora", {
        "08": envio.v8.EnvioDoc,
        "??": envio.v8.EnvioDoc,
    })
    ESTADO = ("Cambios de estado", None)  # noqa: F405
    FACTUL = ("Factura", {
        "01": factul.v1.FacturaDoc,
        "??": factul.v1.FacturaDoc,
    })
    LIBROS = ("Ficha del Libro", {
        "08": libros.v8.LibrosDoc,
        "09": libros.v9.LibrosDoc,
        "10": libros.v10.LibrosDoc,
        "??": libros.v10.LibrosDoc
    })
    LIQVE2 = ("Informe de Liquidación de Ventas",  {
        "02": liqve2.v2.LiquidacionVentaDoc,
        "??": liqve2.v2.LiquidacionVentaDoc
    })
    MENSAJ = ("Mensaje", {
        "01": mensaj.v1.MensajeDoc,
        "??": mensaj.v1.MensajeDoc,
    })
    PEDIDO = ("Albarán de pedido del cliente", {
        "07": pedido.v7.PedidoDoc,
        "??": pedido.v7.PedidoDoc
    })