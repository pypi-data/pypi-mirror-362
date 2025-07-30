from ...document import Document
from ...line import Line
from dataclasses import dataclass
from enum import Enum
from ...common import SinliCode
from ...common import BasicType

@dataclass
class AbonoDoc(Document):
  class Header(Line):
      class Field(Enum):
        TYPE = (0, 1, BasicType.STR,  'Tipo de Registro “C”')
        PROVIDER = (1, 40, BasicType.STR,  "Nombre del proveedor")
        CLIENT = (41, 40, BasicType.STR,  "Nombre del cliente")
        DELIVERY_NUM = (81, 10, BasicType.STR, "Número de albarán")
        DATE = (91, 8, BasicType.DATE,  "Fecha del documento")
        INVOICE_OR_NOTE = (99, 1, SinliCode.INVOICE_OR_NOTE,  'Tipo de documento: “A” | ”F”')
        DEVOLUTION_REFERENCE=(100, 10, BasicType.STR, 'Referencia devolución')
        DEVOLUTION_DATE=(110, 8, BasicType.DATE, 'Fecha devolución')
        PAYMENT_TYPE = (118, 1, SinliCode.PAYMENT_TYPE,  'Tipo de abono: “F” | “D” | “P”')
        BOOK_FAIRE = (119, 1, BasicType.BOOL, '¿Feria del libro? “S” | “N”')
        SHIPPING_COST = (120, 10, BasicType.FLOAT, 'Importe gastos / portes')
        CURRENCY = (130, 1, BasicType.CURRENCY1, 'Moneda, "P" | "E"')

  class Detail(Line):
      class Field(Enum):
          TYPE = (0, 1, BasicType.STR, 'Tipo de Registro, “D”')
          ISBN = (1, 17, BasicType.STR, 'ISBN')
          EAN = (18, 18, BasicType.STR, 'EAN')
          REF = (36, 15, BasicType.STR, 'Referencia')
          TITLE = (51, 50, BasicType.STR, 'Título')
          AMOUNT = (101, 6, BasicType.INT, 'Cantidad')
          PRICE_NO_VAT = (107, 10, BasicType.FLOAT, 'Precio sin IVA')
          PRICE_W_VAT = (117, 10, BasicType.FLOAT, 'Precio con IVA')
          DISCOUNT = (127, 6, BasicType.FLOAT, 'Descuento')
          VAT_PERCENT = (133, 5, BasicType.FLOAT, 'Porcentaje de IVA')
          NEW = (138, 1, BasicType.BOOL, 'Novedad, “S” | ”N”')
          PRICE_TYPE = (139, 1, SinliCode.PRICE_TYPE, 'Tipo de precio, “F” | ”L”')

  class Total(Line):
      class Field(Enum):
          TYPE_REGISTER = (0, 1, BasicType.STR, "Tipo de Registro: T")
          TOTAL_UD = (1, 8, BasicType.INT, "Total unidades")
          TOTAL_DOCUMENT = (9,10, BasicType.FLOAT, "Total documento")

  class VatApportionment(Line):
     class Field(Enum):
        TYPE = (0, 1, BasicType.STR, 'Tipo de registro', 'V')
        VAT_PERCENTAGE = (1, 5, BasicType.FLOAT, 'Porcentaje de IVA')
        TAX_BASE = (6, 10, BasicType.FLOAT, 'Base Imponible')
        VAT = (16, 10, BasicType.FLOAT, 'IVA')
        PERCENTAGE_REQ = (26, 5, BasicType.FLOAT, '% REQ')
        REQ = (31, 10, BasicType.FLOAT, 'REQ')

  class Rejection:
     class Field(Enum):
        TYPE = (0, 1, BasicType.STR, 'Tipo de registro', 'R')
        ISBN = (1, 17, BasicType.STR, 'ISBN')
        EAN = (18, 18, BasicType.STR, 'EAN')
        REF = (36, 15, BasicType.STR, 'Referencia')
        TITLE = (51, 50, BasicType.STR, 'Título')
        REJECTION_CAUSE = (101, 30, BasicType.STR, 'Causa de rechazo')

  linemap = {
        "C": Header,
        "D": Detail,
        "T": Total,
        "V": VatApportionment,
        "R": Rejection,
    }

