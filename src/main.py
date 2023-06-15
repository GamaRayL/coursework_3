import json

from src.utils import *


def main():
    _list = []

    with open("../src/store/operations.json", encoding="utf-8") as file:
        _list = json.load(file)

    print(get_last_operations(_list))


main()
