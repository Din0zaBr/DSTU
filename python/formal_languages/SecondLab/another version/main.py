import re
import grammar_reader
from typing import AnyStr, Pattern


def is_context_independent(args: dict[str, list]) -> bool:
    """
    Пример:
    S -> aSa
    S -> bSb
    S -> aa
    I -> bb
    """
    return _checker(args, re.compile(r'^[A-Z] -> .*$'))


def _checker(grammar: dict[str, list[str]], pattern: Pattern[AnyStr]) -> bool:
    """
    В данную функцию передают саму грамматику, которую пользователь ввел с консоли и паттерн для проверки.
    """
    for first_half, second_half in grammar.items():
        if not all(pattern.fullmatch(f"{first_half} -> {second_half_el}") for second_half_el in second_half):
            return False
    return True


def main(dictionary=None) -> str:
    if dictionary is None:
        dictionary = grammar_reader()

    if is_context_independent(dictionary):
        return "Тип 2: контекстно-свободная грамматика"

    return "Грамматика типа 0"


if __name__ == "__main__":
    print(main())
