from src.utils import *


def main():
    path = "../src/store/operations.json"

    print(get_last_operations(get_data(path)))


main()
