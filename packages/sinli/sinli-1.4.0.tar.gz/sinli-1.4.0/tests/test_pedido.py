import pytest
import datetime
from sinli.document import Document, DocumentVersionError


def test_read_pedido_v7():
    result = Document.from_filename("res/example-sinli-docs/PEDIDO/pedido2.txt")

    assert result.long_id_line.to_dict() == {
        "TYPE": "I",
        "FORMAT": "N",
        "DOCTYPE": "PEDIDO",
        "VERSION": "07",
        "FROM": "L0009999",
        "TO": "L0001234",
        "LEN": 5,
        "NUM_TRANS": 0,
        "LOCAL_FROM": "",
        "LOCAL_TO": "",
        "TEXT": "",
        "FANDE": "FANDE",
    }
    assert result.short_id_line.to_dict() == {
        "TYPE": "I",
        "FROM": "sinli.caixaforum@laie.es",
        "TO": "ejemploejemplo@example.org",
        "DOCTYPE": "PEDIDO",
        "VERSION": "07",
        "TRANSMISION_NUMBER": 0,
    }
    assert [element.to_dict() for element in result.doc_lines] == [
        {
            "TYPE": "C",
            "CUSTOMER": "LAIE",
            "PROVIDER": "EDITORIAL I DISTRIBUIDORA EJEMPLO",
            "ORDER_DATE": datetime.date(2024, 5, 13),
            "ORDER_CODE": "4500081332",
            "ORDER_TYPE": ("N", "Normal"),
            "CURRENCY": "E",
            "PRINT_ON_DEMAND": False,
            "ASKED_DELIVERY_DATE": datetime.date(1970, 1, 1),
            "MAX_DELIVERY_DATE": datetime.date(1970, 1, 1),
            "STRICT_MAX_DELIVERY_DATE": False,
        },
        {
            "TYPE": "E",
            "NAME": "LAIE ALMACEN (MAGATZEM)",
            "ADDRESS": "CALLE TORRASSA 79",
            "POSTAL_CODE": "08930",
            "MUNICIPALITY": "SANT ADRIÀ DEL BESÒS",
            "PROVINCE": "",
        },
        {
            "TYPE": "D",
            "ISBN": "9788412339871",
            "EAN": "9788412339871",
            "REFERENCE": "",
            "TITLE": "BRUJAS CAZA DE BRUJAS Y MUJERES",
            "QUANTITY": 5,
            "PRICE": 14.0,
            "INCLUDE_PENDING": False,
            "ORDER_SOURCE": ("N", "Normal"),
            "EXPRESS": False,
            "ORDER_CODE": "4500081332",
        },
        {
            "TYPE": "D",
            "ISBN": "9788494719615",
            "EAN": "9788494719615",
            "REFERENCE": "",
            "TITLE": "EL FEMINISMO ES PARA TODO EL MUNDO",
            "QUANTITY": 3,
            "PRICE": 12.0,
            "INCLUDE_PENDING": False,
            "ORDER_SOURCE": ("N", "Normal"),
            "EXPRESS": False,
            "ORDER_CODE": "4500081332",
        },
    ]


def test_read_pedido_version_no_soportada():
    with pytest.raises(
        DocumentVersionError,
        match="Tried to parse a PEDIDO message of version 99 with schema 07",
    ):
        Document.from_filename(
            "res/example-sinli-docs/PEDIDO/pedido_version_no_soportada.txt"
        )
