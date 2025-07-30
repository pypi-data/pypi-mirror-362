from ...document import Document
from ...line import Line
from ...common import SinliCode as c
from ...common import BasicType as t
from enum import Enum
from dataclasses import dataclass, field

class LibrosDoc(Document):
    class Header(Line):
        class Field(Enum):
            TYPE = (0, 1, t.STR, "Tipo de Registro")
            PROVIDER = (1, 40, t.STR, "Nombre del proveedor")
            CURRENCY = (41, 1, t.CURRENCY1, "Moneda")

    class Book(Line):
        class Field(Enum):
            EAN = (0, 18, t.STR, "EAN")
            ISBN_INVOICE = (18, 17, t.STR, "ISBN (Con guiones) Facturación")
            ISBN_COMPLETE = (35, 17, t.STR, "ISBN (Con guiones) Obra completa")
            ISBN_VOLUME = (52, 17, t.STR, "ISBN (Con guiones) Tomo")
            ISBN_ISSUE = (69, 17, t.STR, "ISBN (Con guiones) Fascículo")
            REFERENCE = (86, 15, t.STR, "Referencia")
            TITLE_FULL = (101, 80, t.STR, "Título completo")
            SUBTITLE = (181, 80, t.STR, "Subtítulo")
            AUTHORS = (261, 150, t.STR, "Autor/es (Apellidos, Nombre)")
            PUB_COUNTRY = (411, 2, t.COUNTRY, "País de publicación")
            EDITOR_ISBN = (413, 8, t.STR, "Editorial (Código ISBN)")
            EDITOR = (421, 40, t.STR, "Editorial (Nombre)")
            BINDING = (461, 2, c.BINDING, "Código de tipo de encuadernación")
            LANGUAGE = (463, 3, t.LANG, "Lengua de publicación (Código de la tabla ISO 639-2)")
            EDITION = (466, 2, t.STR, "Número de edición")
            PUB_DATE= (468, 6, t.MONTH_YEAR, "Fecha de publicación en formato mmaaaa")
            PAGE_NUM = (474, 4, t.INT, "Número de páginas")
            WIDTH_MM = (478, 4, t.INT, "Ancho en mm.")
            HEIGH_MM = (482, 4, t.INT, "Alto en mm.")
            TOPICS = (486, 20, t.STR, "Temas separados por ';' en códigos CDU o ISBN")
            KEYWORDS = (506, 80, t.STR, "Palabras clave o descriptores, separadas por '/'")
            STATUS = (586, 1, c.STATUS, "Código de situación en catálogo", )
            PRODUCT_TYPE = (587, 2, c.PRODUCT_TYPE, "Código de tipo de producto")
            PRICE_PVP = (589, 10, t.FLOAT, "PVP sin IVA en EUR (sin puntuación)")
            PRICE_PV = (599, 10, t.FLOAT, "PV con IVA en EUR (sin puntuación)")
            TAX_IVA = (609, 5, t.FLOAT, "Porcentaje de IVA (ej: 4, 16, 21, ...)")
            PRICE_TYPE = (614, 1, c.PRICE_TYPE, "Tipo de precio. F = Fijo, L = Libre. Si es L, el precio sin IVA será el precio de cesión, y el precio con IVA, el precio de sesión más el IVA correspondiente")
            COLLECTION = (615, 40, t.STR, "Nombre de la colección")
            COL_NUM = (655, 10, t.STR, "Número de colección")
            VOL_NUM = (665, 4, t.STR, "Número de volumen")
            COVER_IMAGE = (669, 1, t.STR, "Fuente de la imagen de portada y/u otras. N = No; A = Anexada, debe ser en jpg, pesar menos de 500 KB, y el nombre del fichero adjunto con la/las imágenes será el código EAN13; U = URL")
            COVER_ILLUSTRATOR = (670, 150, t.STR, "Lista de ilustradores de la cubierta en formato 'Apellidos, Nombre' y separados por '/'")
            INNER_ILLUSTRATOR = (820, 150, t.STR, "Lista de ilustradores del interior en formato 'Apellidos, Nombre' y separados por '/'")
            COLOR_ILL_NUM = (970, 5, t.INT, "Número de ilustraciones a color")
            TRANSLATORS = (975, 150, t.STR, "Lista de personas traductoras en formato 'Apellidos, Nombre' y separados por '/'")
            LANG_ORIG = (1125, 3, t.LANG, "Idioma original en código ISO 639-2")
            THICK_MM = (1128, 3, t.INT, "Grosor en milímetros")
            WEIGHT_G = (1131, 6, t.INT, "Peso en gramos")
            AUDIENCE = (1137, 3, c.AUDIENCE, "Código de audiencia objetivo")
            READ_LEVEL = (1140, 1, c.READ_LEVEL, "Código de nivel de lectura")
            TB_LEVEL = (1141, 15, t.STR, "Libro de texto: nivel (infantil, primaria, eso, bachillerato, fp, universitaria)")
            TB_COURSE = (1156, 80, t.STR, "Libro de texto: Curso")
            TB_SUBJECT = (1236, 80, t.STR, "Libro de texto: Asignatura")
            TB_REGION = (1316, 36, c.TB_REGION, "Libro de texto: Lista de códigos de comunidades autónoma, separados por '/'.")

            SUMMARY = (1352, 255, t.STR, "Resumen, sinopsis")
            IBIC_VERSION = (1607, 3, t.STR, "iBIC: Tipo de versión. ej: 1.1")
            IBIC_TOPICS = (1610, 50, t.STR, "iBIC: Lista de temas (materias) separados por ';'")
            DATE_LAUNCH = (1660, 8, t.DATE, "Fecha de puesta en venta o lanzamiento, en formato AAAAMMDD")
            DATE_AVAILABLE = (1668, 8, t.DATE, "Fecha de disponibilidad de existencias, en formato AAAAMMDD")
            URL = (1676, 199, t.STR, "Dirección URL. Se recomienda nombrar al menos con el EAN en las primeras posiciones")
            SUMMARY_EXT = (1875, 1125, t.STR, "Resumen o sinopsis ampliadas")

    linemap = {
        "C": Header,
        "": Book
    }
