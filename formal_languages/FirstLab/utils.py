"""
В 1 лабораторной работе происходит запрос грамматики через консоль, поэтому вынес отдельную функцию, чтобы обрабатывать
"""
from collections import defaultdict
import re


def get_rules_from_console(key="remove"):
    """
    Получение информации о правилах грамматики, возвращая в виде словаря
    """
    dictionary = defaultdict(list)
    print("Сейчас вы будете вводить грамматики. Пример ввода: S -> aSb\nКонец ввода - это 'exit' ")

    while (args := input()) != "exit":
        key, value = map(lambda x: x.strip().rstrip("|ε" if key != "don't_remove" else ""), args.split("->"))
        dictionary[key].append(value)

    return dictionary
