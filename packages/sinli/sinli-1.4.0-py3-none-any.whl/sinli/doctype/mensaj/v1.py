from ...document import Document
from ...line import Line
from ...common import BasicType as t
from enum import Enum
from dataclasses import dataclass, field

@dataclass
class MensajeDoc(Document):
    class Header(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR,  'Tipo de Registro “C”')
            DATE = (1, 8, t.DATE,  "Fecha del documento")
            SOURCE_DOC_NUM = (9, 10, t.STR,  "Nº de documento origen")
            RESPONSE_DOC_NUM = (19, 10, t.STR,  "Nº de documento respuesta")

    class Detail(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, 'Tipo de Registro, “D”')
            MSG_BODY = (1, 400, t.STR, 'Cuerpo del mensaje')


