from ...document import Document
from ...line import Line
from ...common import SinliCode as c
from ...common import BasicType as t
from enum import Enum
from dataclasses import dataclass


@dataclass
class PedidoDoc(Document):
    class Header(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, "Tipo de registro")
            CUSTOMER = (1, 40, t.STR, "Nombre del cliente")
            PROVIDER = (41, 40, t.STR, "Nombre del proveedor")
            ORDER_DATE = (81, 8, t.DATE, "Fecha del pedido")
            ORDER_CODE = (89, 10, t.STR, "Código del pedido")
            ORDER_TYPE = (
                99,
                1,
                c.ORDER_TYPE,
                "Tipo del pedido. Valores: N (normal) F (feria/sant jordi) D (depósito) O (otros)",
            )
            CURRENCY = (100, 1, t.CURRENCY1, "Moneda")
            PRINT_ON_DEMAND = (101, 1, t.BOOL, "Impresión bajo demanda: S/N")
            ASKED_DELIVERY_DATE = (102, 8, t.DATE, "Fecha de entrega solicitada")
            MAX_DELIVERY_DATE = (110, 8, t.DATE, "Última fecha de entrega admitida")
            STRICT_MAX_DELIVERY_DATE = (
                118,
                1,
                t.BOOL,
                "Caducidad última fecha entrega: S/N. Si se entrega después del límnite, será rechazada?",
            )

    class DeliveryPlace(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, "Tipo de registro")
            NAME = (1, 50, t.STR, "Nombre del punto de entrega")
            ADDRESS = (51, 80, t.STR, "Dirección")
            POSTAL_CODE = (131, 5, t.STR, "Código postal")
            MUNICIPALITY = (136, 50, t.STR, "Municipio")
            PROVINCE = (186, 40, t.STR, "Provincia")

    class Detail(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, "Tipo de registro")
            ISBN = (1, 17, t.STR, "ISBN")
            EAN = (18, 18, t.STR, "EAN")
            REFERENCE = (36, 15, t.STR, "Reference")
            TITLE = (51, 50, t.STR, "Título")
            QUANTITY = (101, 6, t.INT, "Cantidad")
            PRICE = (107, 10, t.FLOAT, "Precio")
            INCLUDE_PENDING = (117, 1, t.BOOL, "¿Quiere pendientes? S/N")
            ORDER_SOURCE = (
                118,
                1,
                c.ORDER_SOURCE,
                "Origen del pedido: N (normal), C (cliente)",
            )
            EXPRESS = (
                119,
                1,
                t.BOOL,
                "Envío en menos de 24h con gastos de envío especiales S/N",
            )
            ORDER_CODE = (120, 10, t.STR, "Código de pedido")

    class SimpleDetail(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, "Tipo de registro")
            TEXT = (
                1,
                80,
                t.STR,
                "Texto libre. En caso de desconocer los identificadores de los libros",
            )

    class Dropshipping(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, "Tipo de registro")
            FINAL_CLIENT = (1, 50, t.STR, "Destino (particular, colegio, otros)")
            RECEIVER_NAME = (51, 50, t.STR, "Nombre receptor entrega")
            PREFIX = (101, 4, t.STR, "Prefijo. En formato +AAA")
            PHONE = (105, 9, t.STR, "Teléfono, sin puntos ni guiones")
            ADDRESS = (114, 80, t.STR, "Dirección")
            EMAIL = (194, 40, t.STR, "Correo electrónico")
            POSTAL_CODE = (234, 11, t.STR, "Código postal")
            MUNICIPALITY = (244, 50, t.STR, "Localidad")
            PROVINCE = (294, 40, t.STR, "Provincia")
            COUNTRY = (334, 40, t.STR, "País")
            CC = (374, 2, t.COUNTRY, "Código ISO de país")
            OBSERVATIONS = (376, 38, t.STR, "Observaciones")

    linemap = {
        "C": Header,
        "E": DeliveryPlace,
        "D": Detail,
        "M": SimpleDetail,
        "H": Dropshipping,
    }
