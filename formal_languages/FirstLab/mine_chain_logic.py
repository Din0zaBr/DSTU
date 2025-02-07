"""
Здесь реализовано 1 задание, где просят с помощью программного решения создать замену строк, создав свою грамматику.
"""
from typing import Final

RULES: Final = {
    "S": {"1": "aA", "2": "bA"},
    "A": {"1": "+a-b", "2": "+b-a", "3": "+a-a", "4": "+b-b"},
}


def chain_generator(string: str) -> None:
    """
    Функция, которая порождает цепочку, учитывая грамматики
    """
    # Проходимся поэлементно, проверяя, что символы для замены есть в словаре
    for char in string:
        if char in RULES:
            string = string.replace(char, RULES[char][choice_in_dictionary(char)], 1)
            print(" --> ", string)

    # Рекурсивный вызов, если еще есть символы для замены
    if any(char in string for char in RULES):
        chain_generator(string)


def choice_in_dictionary(char: str) -> str:
    """
    Задействована логика проверки
    """
    replacement = None

    while replacement not in RULES[char]:
        replacement = input(f"Выберите на что заменить {char}? {RULES[char]}: ")

        if replacement not in RULES[char]:
            print("Неправильный ввод")

    return replacement


if __name__ == "__main__":
    # Всегда замена начинается с "S"
    chain_generator("S")
