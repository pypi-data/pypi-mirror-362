import datetime
from sinli.document import Document
from pycountry import countries, languages


def test_read_libros_v8():
    result = Document.from_filename("res/example-sinli-docs/libros.txt")

    assert result.long_id_line.to_dict() == {
        "TYPE": "I",
        "FORMAT": "N",
        "DOCTYPE": "LIBROS",
        "VERSION": "08",
        "FROM": "LIB00019",
        "TO": "L0001234",
        "LEN": 0,
        "NUM_TRANS": 0,
        "LOCAL_FROM": "",
        "LOCAL_TO": "",
        "TEXT": "",
        "FANDE": "FANDE",
    }

    assert result.short_id_line.to_dict() == {
        "TYPE": "I",
        "FROM": "fandite@distriforma.es",
        "TO": "ejemploejemplo@example.org",
        "DOCTYPE": "LIBROS",
        "VERSION": "08",
        "TRANSMISION_NUMBER": 0,
    }
    assert len(result.doc_lines) == 6
    assert result.doc_lines[0].to_dict() == {
        "TYPE": "C",
        "PROVIDER": "DISTRIFORMA, S.A.",
        "CURRENCY": "E",
    }

    assert result.doc_lines[1].to_dict() == {
        "EAN": "9788419160867",
        "ISBN_INVOICE": "978-84-19160-86-7",
        "ISBN_COMPLETE": "",
        "ISBN_VOLUME": "",
        "ISBN_ISSUE": "",
        "REFERENCE": "BEL060867",
        "TITLE_FULL": "SUJETOS OBSTINADOS",
        "SUBTITLE": "",
        "AUTHORS": "SARA AHMED",
        "PUB_COUNTRY": countries.get(alpha_2="es"),
        "EDITOR_ISBN": "019160",
        "EDITOR": "EDICIONS BELLATERRA CULTURA21, SCCL",
        "BINDING": ("03", "Rústica"),
        "LANGUAGE": languages.get(alpha_2="es"),
        "EDITION": "",
        "PUB_DATE": datetime.date(2024, 5, 1),
        "PAGE_NUM": 344,
        "WIDTH_MM": 15,
        "HEIGH_MM": 23,
        "TOPICS": "",
        "KEYWORDS": "",
        "STATUS": ("0", "Disponible"),
        "PRODUCT_TYPE": ("10", "libro"),
        "PRICE_PVP": 21.15,
        "PRICE_PV": 22.0,
        "TAX_IVA": 4.0,
        "PRICE_TYPE": ("F", "Precio final fijo"),
        "COLLECTION": "",
        "COL_NUM": "",
        "VOL_NUM": "",
        "COVER_IMAGE": "U",
        "COVER_ILLUSTRATOR": "",
        "INNER_ILLUSTRATOR": "",
        "COLOR_ILL_NUM": 0,
        "TRANSLATORS": "",
        "LANG_ORIG": None,
        "THICK_MM": 0,
        "WEIGHT_G": 250,
        "AUDIENCE": ("000", "Sin calificar"),
        "READ_LEVEL": ("0", "Sin calificar"),
        "TB_LEVEL": "",
        "TB_COURSE": "",
        "TB_SUBJECT": "",
        "TB_REGION": None,
        "SUMMARY": "La obstinación podría considerarse un arte político, un oficio prácti\x02co que se adquiere a través de la participación en la lucha política, ya sea por existir o por transformar una existencia. La historia de la vo\x02luntad es la historia de los intentos por",
        "IBIC_VERSION": "2.1",
        "IBIC_TOPICS": "JHB",
        "DATE_LAUNCH": datetime.date(2024, 5, 8),
        "DATE_AVAILABLE": datetime.date(2024, 5, 8),
        "URL": "http://www.zonalibros.com/img/29/9788419160867.jpg",
        "SUMMARY_EXT": "La obstinación podría considerarse un arte político, un oficio prácti\x02co que se adquiere a través de la participación en la lucha política, ya sea por existir o por transformar una existencia. La historia de la vo\x02luntad es la historia de los intentos por eliminar la obstinación. Pro\x02fundizando en textos filosóficos y literarios, Sara Ahmed examina la relación entre la voluntad y la obstinación, la voluntad particular y la general, y la buena y la mala voluntad. Sus reflexiones arrojan luz sobre cómo la voluntad y la obstinación están integradas en un pai\x02saje político y cultural. Atenta a las consideradas como descarriadas, errantes y desviadas, considera el modo en que la obstinación es ex\x02presada y afecta a aquellas que la adoptan.Aquí, como en sus otras obras conocidas por su originalidad, agu\x02deza y alcance, Ahmed nos ofrece un análisis vibrante y sorprendente de la política basándose en usos eministas, queer y antirracistas de la voluntad y la obstinación para explicar brillantemente el desacuerdo inflexible como parte constitutiva de cualquier ética política radical posible    FECHA VENTA 20 MAYO",
    }
