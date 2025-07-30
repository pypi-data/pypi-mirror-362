from ...document import Document
from ...line import Line
from dataclasses import dataclass
from enum import Enum
from ...common import SinliCode as c
from ...common import BasicType as t

@dataclass
class LiquidacionVentaDoc(Document):
  class Header(Line):
    class Field(Enum):
      TYPE = (0, 1, t.STR,  'Tipo de Registro “C”')
      CLIENT = (1, 40, t.STR,  "Nombre del cliente")
      PROVIDER = (41, 40, t.STR,  "Nombre del proveedor")
      DATE = (81, 8, t.DATE,  "Fecha del documento")
      START_PERIOD_DATE = (89, 8, t.DATE,  "Fecha inicio del periodo")
      END_PERIOD_DATE = (97, 8, t.DATE,  "Fecha final periodo")
      DOCUMENT_NUM = (105, 10, t.STR, 'Nº documento')
      CURRENCY = (125, 1, t.CURRENCY1, 'Moneda, "P" | "E"')

  class Detail(Line):
    class Field(Enum):
      TYPE = (0, 1, t.STR, 'Tipo de Registro, “D”')
      LIQ_TYPE = (1, 1, c.LIQ_TYPE, 'Tipo de Movimiento: Venta, Abono, Obsequio | (V/A/O)')
      ISBN = (2, 17, t.STR, 'ISBN')
      EAN = (19, 18, t.STR, 'EAN')
      REF = (37, 15, t.STR, 'Referencia')
      TITLE = (52, 50, t.STR, 'Título')
      SOLD = (102, 7, t.INT, 'Número de ventas netas')
      PRICE_NO_VAT = (109, 10, t.FLOAT, 'Precio sin IVA')
      PRICE_W_VAT = (119, 10, t.FLOAT, 'Precio con IVA')
      DISCOUNT = (129, 6, t.FLOAT, 'Descuento')
      VAT_PERCENT = (135, 5, t.FLOAT, 'Porcentaje de IVA')

  class Total(Line):
    class Field(Enum):
      TYPE = (0, 1, t.STR, "Tipo de Registro: T")
      TOTAL_UD = (1, 8, t.INT, "Total unidades")
      TOTAL_GROSS = (9, 10, t.FLOAT, 'Total documento BRUTO')
      TOTAL_NET = (19, 10, t.FLOAT, 'Total documento NETO')

  linemap = {
    "C": Header,
    "D": Detail,
    "T": Total,
  }
