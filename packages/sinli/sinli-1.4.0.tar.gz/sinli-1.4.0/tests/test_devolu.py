import datetime
from sinli.document import Document


def test_read_devolu_v2():
    result = Document.from_filename("res/example-sinli-docs/devolu.txt")

    assert result.long_id_line.to_dict() == {
        "TYPE": "I",
        "FORMAT": "N",
        "DOCTYPE": "DEVOLU",
        "VERSION": "02",
        "FROM": "L0009999",
        "TO": "L0001234",
        "LEN": 6,
        "NUM_TRANS": 76650,
        "LOCAL_FROM": "",
        "LOCAL_TO": "",
        "TEXT": "",
        "FANDE": "FANDE",
    }

    assert result.short_id_line.to_dict() == {
        "TYPE": "I",
        "FROM": "llibreriaejemplo@ejemplo.info",
        "TO": "ejemploejemplo@example.org",
        "DOCTYPE": "DEVOLU",
        "VERSION": "02",
        "TRANSMISION_NUMBER": 76650,
    }
    assert [element.to_dict() for element in result.doc_lines] == [
        {
            "TYPE": "C",
            "CLIENT_NAME": "LLIBRERIA EXEMPLE",
            "PROVIDER_NAME": "EDITORIAL EXEMPLE",
            "DELIVERY_NUMBER": "26996",
            "DOCUMENT_DATE": datetime.date(2024, 5, 10),
            "DOCUMENT_TYPE": ("D", "Devolución definitiva"),
            "DEVOLUTION_TYPE": ("D", "Devolución de depósito"),
            "FAIR_BOOK": False,
            "CURRENCY": "E",
        },
        {
            "TYPE": "D",
            "ISBN": "978-84-460-4344-7",
            "EAN": "9788446043447",
            "REFERENCE": "0011040040",
            "TITLE_FULL": "EL LIBRO DE LOS NEGOCIOS",
            "QUANTITY": 1,
            "PRICE": 28.8,
            "PRICE_IVA": 29.95,
            "DESCOUNT": 30.0,
            "PRICE_TYPE": ("L", "Precio final libre"),
            "NOVEDAD": "",
            "DOCUMENT": "",
            "DATE": 0,
            "DEVOLUTION_CAUSE": None,
        },
        {
            "TYPE": "D",
            "ISBN": "978-84-460-4694-3",
            "EAN": "9788446046943",
            "REFERENCE": "0011040056",
            "TITLE_FULL": "EL ÁTOMO",
            "QUANTITY": 1,
            "PRICE": 25.96,
            "PRICE_IVA": 27.0,
            "DESCOUNT": 30.0,
            "PRICE_TYPE": ("L", "Precio final libre"),
            "NOVEDAD": "",
            "DOCUMENT": "",
            "DATE": 0,
            "DEVOLUTION_CAUSE": None,
        },
        {
            "TYPE_REGISTER": "T",
            "TOTAL_UD": 2,
            "TOTAL_DOCUMENT": 56.95,
            "NET_DOCUMENT": 39.87,
            "LUMPS": "",
        },
    ]
