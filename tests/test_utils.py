import pytest

from src.utils import *


def test_get_last_operations():
    input_list = [{
        "id": 147815167,
        "state": "EXECUTED",
        "date": "2018-01-26T15:40:13.413061",
        "operationAmount": {
            "amount": "50870.71",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод с карты на счет",
        "from": "Maestro 4598300720424501",
        "to": "Счет 43597928997568165086"
    }]

    expected_result = "2018.01.26 Перевод организации\n" \
                      "Maestro 4598 30** **** 4501 -> Счет **5086\n" \
                      "50870.71 руб.\n"

    assert get_last_operations(input_list) == expected_result


def test_get_mask_account():
    assert get_mask_account("Счет 43597928997568165086") == "Счет **5086"


def test_get_mask_card():
    assert get_mask_card("Visa Classic 6831982476737658") == "Visa Classic 6831 98** **** 7658"


def test_get_date_reformat():
    assert get_date_reformat("2018-08-19T04:27:37.904916") == "2018.08.19"
    with pytest.raises(ValueError):
        get_date_reformat("2018-08-19 04:27:37.904916")

