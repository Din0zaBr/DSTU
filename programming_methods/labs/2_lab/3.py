"""
Задача №485. Ставки

Перед началом тараканьих бегов всем болельщикам было предложено сделать по две ставки на результаты бегов.
Каждая ставка имеет вид "Таракан №A придет раньше, чем таракан №B".

Организаторы бегов решили выяснить, могут ли тараканы прийти в таком порядке, чтобы у каждого болельщика сыграла
ровно одна ставка из двух (то есть чтобы ровно одно из двух утверждений каждого болельщика оказалось верным).
Считается, что никакие два таракана не могут прийти к финишу одновременно.

Входные данные

В первой строке входных данных содержатся два разделенных пробелом натуральных числа: число K, не превосходящее 10, - количество
тараканов и число N, не превосходящее 100, - количество болельщиков.
Все тараканы пронумерованы числами от 1 до K. Каждая из следующих N строк содержит 4 натуральных числа A, B, C, D,
не превосходящих K, разделенных пробелами. Они соответствуют ставкам болельщика "Таракан №A придет раньше,
чем таракан №B" и "Таракан №C придет раньше, чем таракан №D".

Выходные данные

Если завершить бега так, чтобы у каждого из болельщиков сыграла ровно одна из двух ставок, можно, то следует вывести
номера тараканов в том порядке, в котором они окажутся в итоговой таблице результатов (сначала номер таракана,
пришедшего первым, затем номер таракана, пришедшего вторым и т. д.) в одну строку через пробел.
 Если таких вариантов несколько, выведите любой из них.

Если требуемого результата добиться нельзя, выведите одно число 0.

НЕ ПРОХОДИТ ВСЕ ТЕСТЫ ПО СКОРОСТИ И КОРРЕКТНСОТИ, ВАРИАНТ 100 БАЛЛОВ НА С++
"""
from itertools import permutations
from typing import List, Tuple, Union, cast


def solve(k: int, rates: List[Tuple[int, int, int, int]]) -> Union[List[int], int]:
    """
    Основная идея решения заключается в том, что мы можем использовать брутфорс с оптимизацией:

    Генерируем все возможные порядки финиша тараканов
    Для каждого порядка проверяем, выполняются ли условия задачи
    Возвращаем первый найденный правильный порядок
    :param k: Количество тараканов.
    :param rates: Ставки болельщиков, где каждая ставка - это кортеж из четырех чисел (A, B, C, D).
    :returns: Список номеров тараканов в порядке финиша, если решение возможно. Если невозможно, возвращает 0.
    """
    cockroaches = list(range(1, k + 1))  # Все возможные тараканы

    for perm in permutations(cockroaches):
        valid = True
        for rate in rates:
            a, b, c, d = rate

            # Находим индексы тараканов в текущей перестановке
            idx_a = perm.index(a)
            idx_b = perm.index(b)
            idx_c = perm.index(c)
            idx_d = perm.index(d)

            # Проверка, что ровно одна из ставок выполняется
            condition1 = idx_a < idx_b  # A до B
            condition2 = idx_c < idx_d  # C до D

            # Условие: ровно одно из утверждений должно быть истинным
            if condition1 == condition2:
                valid = False
                break

        if valid:
            return list(perm)

    return 0


def main() -> None:
    k, n = map(int, input().split())
    rates: List[Tuple[int, int, int, int]] = cast(List[Tuple[int, int, int, int]],
                                                  [tuple(map(int, input().split())) for _ in range(n)])

    result = solve(k, rates)

    if result == 0:
        print(0)
    else:
        print(" ".join(map(str, result[::-1])))


if __name__ == "__main__":
    main()