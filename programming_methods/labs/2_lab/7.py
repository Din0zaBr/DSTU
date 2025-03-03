"""
Задача №1. Коровы - в стойла

На прямой расположены стойла, в которые необходимо расставить коров так, чтобы минимальное расcтояние между
коровами было как можно больше.

Входные данные

В первой строке вводятся числа N (2<N<10001) – количество стойл и K (1<K<N) – количество коров.
Во второй строке задаются N натуральных чисел в порядке возрастания – координаты стойл (координаты не превосходят 10^9)

Выходные данные

Выведите одно число – наибольшее возможное допустимое расстояние.
"""
from typing import List, Sequence


def max_distance_between_cows(stalls: Sequence[int], num_cows: int) -> int:
    """
    Здесь задача заключается на бинарный поиск.
    Основная идея в том, что мы расстояние между коровами будем искать, основываясь на координатах.

    left и right инициализируются так, чтобы охватывать диапазон возможных значений минимального расстояния между коровами.
    left начинается с 0, а right — с максимального расстояния между первым и последним стойлом.
    В каждом шаге цикла мы вычисляем mid, который представляет текущее проверяемое минимальное расстояние.

    Поместим 1 корову в самое первое стойло (слева первое).

    Теперь пытаемся разместить наших коров в цикле for.
    Если коров получается разместить, то увеличиваем мин. расстояние.
    В ином, случае увеличиваем максимальное расстояние.

    Когда цикл завершен, left указывает на первое значение, которое не может быть достигнуто.
    То есть, на минимальное расстояние, при котором не удается разместить K коров.
    Получается мы возвращаем прошлый шаг, когда ещё можно было разместить.

    :param stalls: Координаты стойл.
    :param num_cows: Количество коров.
    :returns: Наибольшее возможное допустимое расстояние.
    """

    left: int = 0
    right: int = stalls[-1] - stalls[0] + 1

    while left < right:
        mid: int = (left + right) // 2
        cows_placed: int = 1
        last_placed_stall: int = stalls[0]  # Последнее стойло, в которое была поставлена корова

        for current_stall in stalls[1:]:
            if current_stall - last_placed_stall >= mid:
                cows_placed += 1
                last_placed_stall = current_stall

        if cows_placed >= num_cows:
            left = mid + 1
        else:
            right = mid

    return left - 1


def main() -> None:
    n, k = map(int, input().split())
    stalls: List[int] = list(map(int, input().split()))

    result: int = max_distance_between_cows(stalls, k)
    print(result)


if __name__ == "__main__":
    main()