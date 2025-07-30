from ...document import Document
from ...line import Line
from ...common import SinliCode as c
from ...common import BasicType as t
from enum import Enum
from dataclasses import dataclass, field

# devolucion es 5 a. albarán de devolución y pedido de devolución (cliente - librería a proveedor). pag 16 del doc de sinli
class DevolucionDoc(Document):
    class Header(Line):
        class Field(Enum):
            TYPE=(0, 1, t.STR, "tipo de registro: C")
            CLIENT_NAME=(1, 40, t.STR, "nombre del cliente")
            PROVIDER_NAME=(41, 40, t.STR, "nombre proveedor") 
            DELIVERY_NUMBER=(81, 10, t.STR, "numero de albarán") 
            DOCUMENT_DATE=(91, 8, t.DATE, "Fecha del documento")
            DOCUMENT_TYPE=(99, 1, c.DEVOLUTION_DOC_TYPE, "Tipo de documento: D| P")
            DEVOLUTION_TYPE=(100, 1, c.DEVOLUTION_TYPE, "Tipo de devolución:F|D")
            FAIR_BOOK= (101, 1, t.BOOL, "Feria del libro:S | N")
            CURRENCY= (102, 1, t.CURRENCY1, "P | E")

    class Detail(Line):
        class Field(Enum): 
            # NOM_ANGLES = (POSICIÓ_CALCULADA, LONGITUD=Long., TIPUS=Tipo_Dato, DESCRIPCIO=Campo+Valor)
            TYPE= (0,1, t.STR, "tipo de registro: D")
            ISBN= (1,17, t.STR, "ISBN")
            EAN= (18,18, t.STR,"EAN")
            REFERENCE= (36,15,t.STR, "referencia")
            TITLE_FULL=(51,50, t.STR, "titulo")
            QUANTITY=(101,6, t.INT, "cantidad")
            PRICE=(107,10, t.FLOAT, "precio sin iva")
            PRICE_IVA=(117,10, t.FLOAT, "precio con iva")
            DESCOUNT= (127,6, t.FLOAT, "descuento")
            PRICE_TYPE=(133,1, c.PRICE_TYPE,"tipo de precio: F|L")
            NOVEDAD= (134,1, t.STR, "novedad")
            DOCUMENT=(135,10, t.STR, "documento de compra")
            DATE=(145,8, t.INT, "fecha de compra")
            DEVOLUTION_CAUSE=(153,1,c.DEVOLUTION_CAUSE, "causa de devolucion")


    class Total(Line):
        class Field(Enum):
            TYPE_REGISTER = (0, 1, t.STR, "Tipo de Registro: T")
            TOTAL_UD = (1, 8, t.INT, "total unidades")
            TOTAL_DOCUMENT = (9,10, t.FLOAT, "total documento bruto")
            NET_DOCUMENT=(19,10, t.FLOAT,"total documento neto")
            LUMPS=(29,3,t.STR, "numero de bultos")


    linemap = {
        "C": Header,
        "D": Detail,
        "T": Total
    }

