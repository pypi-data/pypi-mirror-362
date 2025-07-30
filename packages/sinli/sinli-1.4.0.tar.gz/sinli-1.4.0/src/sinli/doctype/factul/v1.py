from ...document import Document
from ...line import Line
from ...common import SinliCode as c
from ...common import BasicType as t
from enum import Enum
from dataclasses import dataclass, field

@dataclass
class FacturaDoc(Document):
    class Header(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR,  'Tipo de Registro “C”')
            PROVIDER = (1, 40, t.STR,  "Nombre del proveedor")
            CLIENT = (41, 40, t.STR,  "Nombre del cliente")
            INVOICE_NUM = (81, 10, t.STR, "Número de factura")
            DATE = (91, 8, t.DATE,  "Fecha de la factura")
            CURRENCY = (99, 1, t.CURRENCY1, 'Moneda')

    class Detail(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “D”')
            NOTE_NUM = (1, 10, t.STR, 'Número de albarán')
            DATE = (11, 8, t.DATE,  "Fecha")
            AMOUNT = (19, 10, t.FLOAT, "Importe")

    class DetailVat(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “E”')
            NOTE_NUM = (1, 10, t.STR, 'Número de albarán')
            VAT_PERCENT = (11, 5, t.FLOAT, "Porcentaje de IVA")
            VAT_BASE = (16, 10, t.FLOAT, "Base imponible")
            VAT = (26, 10, t.FLOAT, "IVA")
            FEE_PERCENT = (36, 5, t.FLOAT, "Porcentaje Recargo")
            REQ = (41, 10, t.INT, "REQ")

    class Sum(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “T”')
            TOTAL_PRICE = (1, 10, t.FLOAT, 'Importe total del documento')

    class Vat(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “V”')
            VAT_PERCENT = (1, 5, t.FLOAT, "Porcentaje de IVA")
            VAT_BASE = (6, 10, t.FLOAT, "Base imponible")
            VAT = (16, 10, t.FLOAT, "IVA")
            FEE_PERCENT = (26, 5, t.FLOAT, "Porcentaje Recargo")
            REQ = (31, 10, t.INT, "REQ")

    class DueDate(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “P”')
            PAYMENT_TIME = (1, 1, c.PAYMENT_TIME, 'Forma de pago')
            AMOUNT = (2, 10, t.FLOAT, "Importe")
            DUE_DATE = (12, 8, t.DATE, "Fecha de vencimiento")
            COMMENT = (20, 40, t.STR, "Observaciones")



    linemap = {
        "C": Header,
        "D": Detail,
        "E": DetailVat,
        "T": Sum,
        "V": Vat,
        "P": DueDate,
    }
