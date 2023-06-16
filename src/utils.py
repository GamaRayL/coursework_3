import json
from datetime import datetime


def get_last_operations(_list):
    """
    Функция сортирует и возвращает последние 5ть операций клиентов банка.
    ps если же конечно пройдут условие на наличие свойств в словаре.
    :param _list: список словарей
    :return: возврат последних операций
    """
    sorted_list = sorted(_list, key=lambda x: x.get("date", ""), reverse=True)

    count = 0
    result = []

    for item in sorted_list:
        if count == 5:
            break
        if "state" in item and "EXECUTED" == item["state"]:

            date = get_date_reformat(item["date"])
            account = item["to"]
            card = item.get("from", None)
            amount = item["operationAmount"]["amount"]
            currency = item["operationAmount"]["currency"]["name"]
            description = item["description"]

            if get_mask_account(account) is not None:
                count += 1

                result.append(f"{date} {description}")
                result.append(f"{get_mask_card(card)} -> {get_mask_account(account)}")
                result.append(f"{amount} {currency}\n")

    return "\n".join(result)


def get_date_reformat(value):
    """
    Реформат даты
    :param value: значение в формате "%Y-%m-%dT%H:%M:%S.%f"
    :return: возврат в формате "%Y.%m.%d"
    """
    try:
        date_time_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        date_time_str = date_time_obj.strftime("%Y-%m-%d").replace("-", ".")

        return date_time_str
    except ValueError:
        raise ValueError("Некорректный формат даты. Ожидаемый формат '%Y-%m-%dT%H:%M:%S.%f'")


def get_mask_card(value):
    """
    Функция возвращает преобразованный номер карты, основываясь на отсутствии "счет" в строке.
    :param value: строка
    :return: замаскированный номер карты / "Источник перевода отсутствует" /
    """
    if value is None:
        return "Источник перевода отсутствует"
    if "счет" not in value.lower():
        card_split = value.split(" ")
        card_number = card_split[-1]
        card_name = " ".join(card_split[:-1])

        card_number = [card_number[i:i + 4] for i in range(0, 16, 4)]
        card_number[1] = card_number[1][:2] + "**"
        card_number[2] = "****"

        number_mask = " ".join(card_number)

        return f"{card_name} {number_mask}"
    return "Некорректный номер"


def get_mask_account(value):
    """
    Функция возвращает преобразованный номер счета, основываясь на наличии "счет" в строке.
    :param value: строка
    :return: замаскированный счет
    """
    if "счет" in value.lower():
        account_split = value.split(" ")
        account_number = account_split[-1][-4:]
        account_name = " ".join(account_split[:-1])

        return f'{account_name} **{account_number}'


def get_data(path):
    _list = []

    with open(path, encoding="utf-8") as file:
        _list = json.load(file)

        return _list
