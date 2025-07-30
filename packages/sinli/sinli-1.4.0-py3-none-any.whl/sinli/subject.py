#from .document import Document
#from .doctype import DocumentType
from .line import Line
from .common.encoded_values import SinliCode as c, BasicType as t
from .doctype import DocumentType

from enum import Enum
from dataclasses import dataclass, field

@dataclass
class Subject(Line):
    """
    El asunto o subject del mensaje contendrá:
    ESFANDE 7A, Identificador emisor 8A, ESFANDE 7A, Identificador destino 8A,
    Documento 6A, Versión Identificador 2N, FANDE 5A

    Ejemplo:
    ESFANDELIBXXXXXESFANDELIBXXXXXENVIO NNFANDE
    0123456789012345678901234567890123456789012
    0        10        20        30        40
    """
    doctype_desc = ""
    doctype_class = None

    class Field(Enum):
        FILLING1 = (0, 7, t.STR, "ESFANDE")
        FROM     = (7, 8, t.STR, "Sinli From Id")
        FILLING2 = (15, 7, t.STR, "ESFANDE")
        TO       = (22, 8, t.STR, "Sinli To Id")
        DOCTYPE  = (30, 6, t.STR, "Tipo de Fichero")
        VERSION  = (36, 2, t.INT, "Versión fichero")
        FILLING3 = (38, 5, t.STR, "FANDE")

    def __post_init__(self):
        super().__post_init__()
        self.FILLING1 = "ESFANDE"
        self.FILLING2 = "ESFANDE"
        self.FILLING3 = "FANDE"

    def is_valid(self):
        """
        Check if all parameters are set with a minimum of requirements.
        We need a method like this here because Line's in general must be lax
        in what they accept, that is, many fields may be blank and that's ok,
        the only room for improving this check at line parsing is to capture
        Errors and instead, return some Result<Line, Error>, for instance.
        """
        _is_valid = False
        try:
            _is_valid = len(self.FROM) == 8 and \
            len(self.TO) == 8 and \
            self.DOCTYPE != None and self.DOCTYPE != "" and \
            self.VERSION != None and self.VERSION != 0 and \
            self.get_doctype_desc() != "" and \
            self.get_doctype_class() != ""
        except:
            return False
        return _is_valid

    def get_doctype_desc(self) -> str:
        if self.doctype_desc == "":
            self.doctype_desc = getattr(DocumentType, self.DOCTYPE).value[0]

        return self.doctype_desc

    def get_doctype_class(self) -> str:
        if self.doctype_class == None:
            val = getattr(DocumentType, self.DOCTYPE).value
            self.doctype_class = val[1].get(self.VERSION) or val[1].get('??')

        return self.doctype_class

