from datetime import datetime


def get_last_operations(_list):
    sorted_list = sorted(_list, key=lambda x: x.get("date", ""))

    count = 0
    result = []

    for item in sorted_list:
        if count == 5:
            break
        if "state" in item and "EXECUTED" == item["state"] and "from" in item:

            date = get_date_reformat(item["date"])
            card, account = item["from"], item["to"]
            amount = item["operationAmount"]["amount"]
            currency = item["operationAmount"]["currency"]["name"]

            if get_mask_account(account) is not None and get_mask_card(card) is not None:
                count += 1

                result.append(f"{date} Перевод организации")
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
    if "счет" in value.lower():
        return None
    else:
        card_split = value.split(" ")
        card_number = card_split[-1]
        card_name = " ".join(card_split[:-1])

        card_number = [card_number[i:i + 4] for i in range(0, 16, 4)]
        card_number[1] = card_number[1][:2] + "**"
        card_number[2] = "****"

        number_mask = " ".join(card_number)

        return f"{card_name} {number_mask}"


def get_mask_account(value):
    if "счет" in value.lower():
        account_split = value.split(" ")
        account_number = account_split[-1][-4:]
        account_name = " ".join(account_split[:-1])

        return f'{account_name} **{account_number}'


print(get_last_operations([{
    "id": 317987878,
    "state": "EXECUTED",
    "date": "2018-01-13T13:00:58.458625",
    "operationAmount": {
        "amount": "55985.82",
        "currency": {
            "name": "USD",
            "code": "USD"
        }
    },
    "description": "Перевод с карты на карту",
    "from": "Visa Classic 8906171742833215",
    "to": "Cчет 6086997013848217"
},{
    "id": 317987878,
    "state": "EXECUTED",
    "date": "2018-01-13T13:00:58.458625",
    "operationAmount": {
        "amount": "55985.82",
        "currency": {
            "name": "USD",
            "code": "USD"
        }
    },
    "description": "Перевод с карты на карту",
    "from": "Visa Classic 8906171742833215",
    "to": "Cчет 6086997013848217"
}]))
