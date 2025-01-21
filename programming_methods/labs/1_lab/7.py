"""
Задача №500. Парикмахерская

В парикмахерской работают три мастера. Каждый тратит на одного клиента ровно полчаса, а затем сразу переходит к
следующему, если в очереди кто-то есть, либо ожидает, когда придет следующий клиент.

Даны времена прихода клиентов в парикмахерскую (в том порядке, в котором они приходили).
Требуется для каждого клиента указать время, когда он выйдет из парикмахерской.

Входные данные

В первой строке вводится натуральное число N, не превышающее 100 – количество клиентов.
N строках вводятся времена прихода клиентов – по два числа, обозначающие часы и минуты (часы – от 0 до 23, минуты – от 0 до 59).
Времена указаны в порядке возрастания (все времена различны).

Гарантируется, что всех клиентов успеют обслужить до полуночи.

Выходные данные

Требуется вывести N пар чисел: времена выхода из парикмахерской 1-го, 2-го, …, N-го клиента (часы и минуты).
"""
from typing import List, Tuple, cast, Iterable
from collections import deque


def calculate_exit_times(arrival_times: Iterable[Iterable[int, int]]) -> Iterable[Iterable[int, int]]:
    """
    Из условия задачи известно, что всего суммарно 3 мастера, поэтому был создан список, содержащий три нуля.
    Каждый клиент у нас стрижется по 30 минут.

    Если у нас есть свободный мастер, то сразу увеличиваем время на 30 минут относительно времени прихода клиента.
    В ином случае клиенту надо подождать, и мастер сразу начнет стричь его. Поэтому мы к его окончанию добавляем 30 минут.

    Дальше мы просто в дек сохраняем времена для вывода на консоль.

    :param arrival_times: Объект с временами прихода клиентов – по два числа, обозначающие часы и минуты
    (часы – от 0 до 23, минуты – от 0 до 59). Времена указаны в порядке возрастания (все времена различны).

    :returns: Итерируемый объект, по которому можно пройтись для вывода на консоль.
    """
    workers_time: List[int] = [0, 0, 0]
    exit_times: deque[Tuple[int, int]] = deque()

    for hours, minutes in arrival_times:
        arrival_time_in_minutes = hours * 60 + minutes
        # Находим мастера, который свободен раньше всего
        next_worker_index = workers_time.index(min(workers_time))

        # Если мастер свободен до прихода клиента, обновляем его время
        if workers_time[next_worker_index] <= arrival_time_in_minutes:
            workers_time[next_worker_index] = arrival_time_in_minutes + 30
        else:
            workers_time[next_worker_index] += 30  # Мастер начинает работать сразу после завершения

        # Сохраняем время выхода клиента в формате (часы, минуты)
        exit_time = workers_time[next_worker_index]
        exit_times.append((exit_time // 60, exit_time % 60))

    return exit_times


def main() -> None:
    n: int = int(input())
    arrival_times: List[Tuple[int, int]] = cast(
        List[Tuple[int, int]],
        [tuple(map(int, input().split())) for _ in range(n)]
    )

    exit_times: Iterable[Iterable[int, int]] = calculate_exit_times(arrival_times)

    for hours, minutes in exit_times:
        print(hours, minutes)


if __name__ == '__main__':
    main()