from .common.encoded_values import SinliCode as c, BasicType as t, EncodedField
from enum import Enum
from typing_extensions import Self
from dataclasses import dataclass
from pycountry import countries, languages, currencies
from datetime import date
from datetime import datetime

@dataclass(repr=False)
class Line:
    country_class = countries.get(alpha_2="es").__class__
    lang_class = languages.get(alpha_3="cat").__class__
    currency_class = currencies.get(alpha_3="EUR").__class__

    class Field(Enum):
        EXAMPLE = (1, 7, t.STR, "Example field located in 1st position with length 7")

    def __post_init__(self):
        """Initialize all fields with default values"""
        for field in self.Field:
            f_type = field.value[2]
            if f_type == t.STR:
                defval = ""
            elif f_type in [t.INT, t.FLOAT]:
                defval = 0
            elif f_type in [t.DATE, t.MONTH_YEAR]:
                defval = date.fromtimestamp(0)
            # exclude booleans and coded types, as we can't guess
            # which is the safe default value
            else:
                defval = ""

            setattr(self, field.name, defval)


    def __str__(self) -> str:
        """Export to SINLI string"""

        field_l = []
        for field in self.Field:
            deflen = field.value[1]
            f_type = field.value[2]
            val = self.encode(deflen, getattr(self, field.name), f_type)
            vallen = len(val)

            if vallen < deflen:
                if f_type in [t.INT, t.FLOAT]:
                    padding = "0" # pad left with zeroes
                    val = "".join([padding for i in range(0, deflen-vallen)]) + val
                else:
                    padding = " " # pad right with spaces
                    val = val + "".join([padding for i in range(0, deflen-vallen)])
            elif vallen > deflen: # truncate
                print(f"[WARN] Unexpected: field {field.name}={val} shouldn't have been longer than {deflen} chars. Truncating to {val[0:deflen]}")
                val = val[0:deflen]

            field_l.append(val)

        return "".join(field_l)

    def to_csv(self) -> str:
        return ", ".join(vars(self).values())

    def __repr__(self) -> str:
        return repr(vars(self))

    def to_readable(self) -> Self:
        """
        Returns a new dictionary with "pretified" values, that is,
        resolved from sinli codes
        """
        ld = vars(self)
        newld = {}
        for k,v in ld.items():
            newld[k] = self.pretify(k,v)
        line = self.__class__()
        return line.from_dict(newld)

    # Import
    def from_dict(self, fields: {}):
        for (key, value) in fields.items():
            setattr(self, key, value)
        return self

    def to_dict(self) -> dict:
        return vars(self)

    @classmethod
    def from_str(cls, line_s: str) -> Self:
        line_dict = {}
        for field in cls.Field:
            start = field.value[0]
            end = start + field.value[1]
            vtype = field.value[2]
            try:
                line_dict[field.name] = cls.decode(vtype, line_s[start:end].strip())
            except ValueError as err:
                print(f"[ERROR] Decode error. {field} with value \"{line_s[start:end]}\" can't be converted to a float or int.", err)
                line_dict[field.name] = 0
            except NameError as err:
                print(f"[ERROR] Decode error. {field} with value \"{line_s[start:end]}\" can't be converted to a language, currency or country.", err)
                line_dict[field.name] = None

            print(f"[DEBUG] {field} → {line_dict[field.name]}")
        line = cls()
        return line.from_dict(line_dict)

    @staticmethod
    def decode(vtype, value) -> object:
        """
        Convert from a sinli field string to a richer type when it applies:
        it returns a str, int, or date.
        """
        #print(f"vtype: {vtype}, value: {value}")
        if vtype == t.STR:
            return value
        elif vtype == t.INT:
            return int(value or '0')
        elif vtype == t.FLOAT:
            return float(value or '0')/100
        elif vtype == t.BOOL:
            return True if value == "S" else False # "N"
        elif vtype == t.MONTH_YEAR:
            return datetime.strptime(value or "011970", "%m%Y").date()
        elif vtype == t.DATE:
            return datetime.strptime(value or "19700101", "%Y%m%d").date()
        elif vtype == t.LANG:
            return languages.get(alpha_3 = value)
        elif vtype == t.COUNTRY:
            return countries.get(alpha_2 = value)
        elif vtype == t.CURRENCY1:
            return value # TODO understand meaning of P or E values
        elif vtype == t.CURRENCY3:
            return currencies.get(alpha_3 = value)
        elif isinstance(vtype, EncodedField):
            return vtype.decode(value) or None
        else:
            print(f"[WARN] Unexpected case: var {value} is of type {vtype}")
            return value

    @classmethod
    def encode(cls, vlen, value, ftype) -> str:
        """
        Convert an attribute from an object to a string, appendable to a sinli line
        """
        if type(value) == datetime:
            value = value.date()
        if type(value) == float:
            return str(int(value * 100))
        elif type(value) == date:
            if vlen == 6: return value.strftime("%m%Y")
            elif vlen == 8: return value.strftime("%Y%m%d")
            else: raise(f"BUG! unexpected situation to SINLI-encode {value} to a length of {vlen} bytes")
        elif type(value) == bool:
            return "S" if value == True else "N" # value == False
        elif type(value) == cls.country_class:
            return value.alpha_2
        elif type(value) == cls.lang_class:
            return value.alpha_3
        elif type(value) == cls.currency_class:
            if vlen == 3:  return value.alpha_3
            #elif vlen == 1: return value # TODO understand P and E values
        elif isinstance(ftype, EncodedField):
            if value == None or value == "":
                return " "
            return value[0]
        else: # string, integer
            return str(value)

    @classmethod
    def pretify(cls, k, v) -> str:
        """
        pretify field with name k and value v.
        it resolves the sinli codes to their description value,
        sinli codes have the same key as line field keys
        """
        if type(k) == cls.currency_class:
            return v.name
        try:
            return v[1] or "Unknown"
        except:
            return str(v)

class LongIdentificationLine(Line):
    def __post_init__(self):
        super().__post_init__()
        self.TYPE = "I"
        self.FORMAT = "N"

    class Field(Enum):
        TYPE = (0, 1, t.STR, "Tipo de registro (I)")
        FORMAT = (1, 1, t.STR, "Tipo de formato (N=Normalizado ; ?=Libre)")
        DOCTYPE = (2, 6, t.STR, "Nombre del tipo de documento")
        VERSION = (8, 2, t.STR, "Versión del tipo de documento")
        FROM = (10, 8, t.STR, "Identificador ESFANDE del remitente")
        TO = (18, 8, t.STR, "Identificador ESFANDE del destinatario")
        LEN = (26, 5, t.INT, "Cantidad de registros del fichero")
        NUM_TRANS = (31, 7, t.INT, "Número de transmisión s/emisor")
        LOCAL_FROM = (38, 15, t.STR, "Usuario local del emisor")
        LOCAL_TO = (53, 15, t.STR, "Usuario local del destino")
        TEXT = (68, 7, t.STR, "Texto libre")
        FANDE = (75, 5, t.STR, "FANDE")

class ShortIdentificationLine(Line):
    def __post_init__(self):
        super().__post_init__()
        self.TYPE = "I"

    class Field(Enum):
        TYPE = (0, 1, t.STR, "Tipo de registro (I)")
        FROM = (1, 50, t.STR, "E-mail origen")
        TO = (51, 50, t.STR, "E-mail destino")
        DOCTYPE = (101, 6, t.STR, "Tipo de Fichero")
        VERSION = (107, 2, t.STR, "Versión fichero")
        TRANSMISION_NUMBER = (109, 8, t.INT, "Nº de transmisión emisor")
