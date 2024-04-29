from collections import defaultdict


# Функция для ввода грамматик
def grammar_reader():
    print("Для окончания ввода введите end\nВведите грамматику вида S -> aSb: ")

    dictionary = defaultdict(list)

    while (args := input()) != "end":
        key, values = map(lambda x: x.strip(), args.split("->"))
        for value in values.split('|'):
            dictionary[key].append(value.strip())

    return dictionary

