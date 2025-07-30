from ...document import Document
from ...line import Line
from ...common import SinliCode as c
from ...common import BasicType as t
from enum import Enum
from dataclasses import dataclass, field

@dataclass
class EnvioDoc(Document):
    class Header(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR,  'Tipo de Registro “C”')
            PROVIDER = (1, 40, t.STR,  "Nombre del proveedor")
            CLIENT = (41, 40, t.STR,  "Nombre del cliente")
            DELIVERY_NUM = (81, 10, t.STR, "Número de albarán")
            DATE = (91, 8, t.DATE,  "Fecha del documento")
            INVOICE_OR_NOTE = (99, 1, c.INVOICE_OR_NOTE,  'Tipo de documento: “A” | ”F”')
            CONSIGNMENT_TYPE = (100, 1, c.CONSIGNMENT_TYPE,  'Tipo de envío: “F” | “D” | “C”| ”P”')
            BOOK_FAIRE = (101, 1, t.BOOL, '¿Feria del libro? “S” | “N”')
            SHIPPING_COST = (102, 10, t.FLOAT, 'Importe gastos / portes')
            CURRENCY = (112, 1, t.CURRENCY1, 'Moneda')
            FINAL_USER_MAILBOX = (113, 8, t.STR, 'Buzón usuario final')

    class Detail(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “D”')
            ISBN = (1, 17, t.STR, 'ISBN')
            EAN = (18, 18, t.STR, 'EAN')
            REF = (36, 15, t.STR, 'Referencia')
            TITLE = (51, 50, t.STR, 'Título')
            AMOUNT = (101, 6, t.INT, 'Cantidad')
            PRICE_NO_VAT = (107, 10, t.FLOAT, 'Precio sin IVA')
            PRICE_W_VAT = (117, 10, t.FLOAT, 'Precio con IVA')
            DISCOUNT = (127, 6, t.FLOAT, 'Descuento')
            VAT_PERCENT = (133, 5, t.FLOAT, 'Porcentaje de IVA')
            NEW = (138, 1, t.BOOL, 'Novedad, “S” | ”N”')
            PRICE_TYPE = (139, 1, c.PRICE_TYPE, 'Tipo de precio, F (fijo)" | "L (libre)')
            RETURN_MAX_DATE = (140, 8, t.DATE, 'Fecha tope devolución')
            ORDER_CODE = (148, 10, t.STR, 'Código de pedido')
            AUTHORS = (158, 150, t.STR, 'Autor/es (Apellidos, Nombre), Más de un autor separados por barra (/)')
            FREE_PRICE_TYPE = (308, 1, c.FREE_PRICE_TYPE, 'Tipo de precio libre, C (coste) | R (recomendado)')

    class FreeDetail(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “M”')
            TEXT = (1, 80, t.STR, 'Texto')

    class Sum(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “T”')
            TOTAL_UNITS = (1, 8, t.INT, 'Total unidades')
            TOTAL_PRICE_GROSS = (9, 10, t.FLOAT, 'Total precio documento bruto')
            TOTAL_PRICE_NET = (9, 10, t.FLOAT, 'Total precio documento neto')

    class Vat(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “V”')
            VAT_PERCENT = (1, 5, t.FLOAT, "Porcentaje de IVA")
            VAT_BASE = (6, 10, t.FLOAT, "Base imponible")
            VAT = (16, 10, t.FLOAT, "IVA")
            FEE_PERCENT = (26, 5, t.FLOAT, "Porcentaje Recargo")
            REQ = (31, 10, t.INT, "REQ")

    class Status(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “E”')
            ISBN = (1, 17, t.STR, 'ISBN')
            EAN = (18, 18, t.STR, 'EAN')
            REF = (36, 15, t.STR, 'Referencia')
            TITLE = (51, 50, t.STR, 'Título')
            STATUS = (101, 1, t.INT, 'Código de estado según la tabla de situaciones') # FIXME implementa enum "tabla de situaciones"
            REMOVE_PENDING = (102, 1, t.BOOL, 'Elimina pendientes? S | N')
            DATE_APROX = (103, 8, t.DATE, 'Fecha aprox. servicio')

    linemap = {
        "C": Header,
        "D": Detail,
        "M": FreeDetail,
        "T": Sum,
        "V": Vat,
        "E": Status,
    }

