"""
Задача №774. Шифровка

Шпион Коля зашифровал и послал в центр радиограмму.
Он использовал такой способ шифровки: сначала выписал все символы своего сообщения (включая знаки препинания и т.п.),
стоявшие на четных местах, в том же порядке, а затем – все символы, стоящие на нечетных местах.
Напишите программу, которая расшифровывает сообщение.

Входные данные

Вводится одна непустая строка длиной не более 250 символов – зашифрованное сообщение.
Строка может состоять из любых символов, кроме пробельных.

Выходные данные

Выведите одну строку – расшифрованное сообщение.
"""
from typing import List, AnyStr


def decrypt_message(encrypted_message: AnyStr) -> AnyStr:
    """
    Коля начинает нумерацию не с 0, а с 1!

    Из условия задачи известно, что сначала в закодированном стоят четные, а потом уже нечетные.
    Получается сосед текущей буквы будет через половину длины от сообщения.

    :param encrypted_message: Сообщение, которое мы хотим расшифровать по условию задания.
    :returns: Расшифрованное сообщение
    """
    symbols: List[AnyStr] = list()
    n: int = len(encrypted_message) // 2
    for i in range(n):
        symbols += encrypted_message[i + n], encrypted_message[i]
        # symbols[2 * i: 2 * i + 2] = encrypted_message[i + n], encrypted_message[i]
    return ''.join(symbols)


def main() -> None:
    encrypted_message = input()

    decrypted_message: str = decrypt_message(encrypted_message)

    print(decrypted_message)


if __name__ == '__main__':
    main()